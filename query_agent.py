import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from personality import get_animal_prefix, add_fun_fact, get_quirky_intro
from chat_history import load_history, add_to_history

load_dotenv()

CHROMA_DB_PATH = "wildlife_db"
COLLECTION_NAME = "kenya_wildlife_corpus"
EMBEDDING_MODEL = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    transport="rest"
)

# --- ENHANCED RAG PROMPT FOR WILDLIFE EXPERT ---
RAG_PROMPT_TEMPLATE = """
**ROLE:** You are Akoth, a friendly and enthusiastic wildlife expert specializing in the Maasai Mara and Kenyan wildlife! You're passionate about animals, conservation, and sharing fascinating facts with visitors.

**PERSONALITY:** You're warm, engaging, and love to sprinkle in fun facts. You speak like a knowledgeable safari guide who genuinely loves her job. Use emojis occasionally (🦁🦒🐘) to add personality, but don't overdo it.

**TASK:** Answer the user's question about wildlife, animals, or the Maasai Mara using the context provided below.

**INSTRUCTIONS:**
1. Use the provided context fragments to answer the user's question.
2. Make your response engaging and conversational - imagine you're talking to someone on a safari!
3. If you can answer from the context, provide interesting details and fun facts.
4. Structure longer responses with clear sections, but keep the tone friendly and accessible.
5. If the context doesn't fully answer the question but has related info, share what you know and be honest about the gaps.

--- CONTEXT FRAGMENTS ---
{context}

--- USER QUESTION ---
{query}

--- YOUR RESPONSE ---
"""

# --- FALLBACK PROMPT (When no relevant context found) ---
FALLBACK_PROMPT_TEMPLATE = """
**ROLE:** You are Akoth, a friendly wildlife expert for the Maasai Mara and Kenyan wildlife.

**SITUATION:** The user asked a question, but your specific database doesn't have detailed information about it.

**OPENING LINE:** {intro}

**TASK:** Give a helpful, friendly response that:
1. Acknowledges you don't have specific info in your current database
2. If it's wildlife-related, share general knowledge you have about the topic
3. If it's completely unrelated to wildlife/Kenya, gently redirect them back to wildlife topics
4. Always maintain a warm, safari guide personality

**USER QUESTION:** {query}

**AKOTH'S RESPONSE:**
"""

# --- Retriever ---
def create_retriever():
    if not os.path.exists(CHROMA_DB_PATH):
        raise FileNotFoundError(f"Vector database not found at {CHROMA_DB_PATH}")
    db = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=EMBEDDING_MODEL,
        collection_name=COLLECTION_NAME
    )
    return db.as_retriever(search_kwargs={"k": 4})

def check_context_relevance(context_docs, query):
    if not context_docs:
        return False
    combined_text = " ".join([doc.page_content for doc in context_docs])
    return len(combined_text) > 100

# --- RAG / Fallback Runner ---
def run_agent(user_query: str):
    try:
        retriever = create_retriever()

        # Use .retrieve() instead of get_relevant_documents()
        try:
            context_docs = retriever.retrieve(user_query)
        except AttributeError:
            # Older versions fallback
            context_docs = []

        if check_context_relevance(context_docs, user_query):
            rag_prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
            rag_chain = (
                {"context": lambda x: context_docs, "query": RunnablePassthrough()}
                | rag_prompt
                | llm
                | StrOutputParser()
            )
            response = rag_chain.invoke(user_query)
        else:
            quirky_intro = get_quirky_intro()
            fallback_prompt = ChatPromptTemplate.from_template(FALLBACK_PROMPT_TEMPLATE)
            fallback_chain = (
                {"query": RunnablePassthrough(), "intro": lambda x: quirky_intro}
                | fallback_prompt
                | llm
                | StrOutputParser()
            )
            response = fallback_chain.invoke(user_query)

        # Post-process with fun facts / animal prefixes
        response = get_animal_prefix(user_query) + response
        response = add_fun_fact(response)

        # Save to history
        add_to_history(user_query, response)

        return response

    except Exception as e:
        # Friendly fallback message
        return "🦁 Oops — Akoth lost the signal on the savanna! Try asking your question differently. 🌿"

# --- Main Loop ---
if __name__ == "__main__":
    print("🦁 Welcome to Maasai Mara Wildlife Chat! Akoth at your service!\nType 'history' to see recent questions. Type 'exit' to quit.\n")
    while True:
        user_query = input("🌿 Your Question: ").strip()
        if user_query.lower() in ["exit", "quit"]:
            print("🦁 Goodbye! Keep exploring the wild!")
            break
        elif user_query.lower() in ["history", "recent"]:
            history = load_history()
            if not history:
                print("📜 No previous questions yet!\n")
            else:
                print("\n📜 Recent Questions & Answers:")
                for i, qa in enumerate(history[-5:], 1):
                    print(f"{i}. Q: {qa['question']}\n   A: {qa['answer']}\n")
            continue
        elif not user_query:
            print("💭 Please enter a question.\n")
            continue

        response = run_agent(user_query)
        print("\n" + "="*60)
        print(response)
        print("="*60 + "\n")