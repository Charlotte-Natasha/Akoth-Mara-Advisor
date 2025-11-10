import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- CONFIGURATION (Must match your indexing script) ---
CHROMA_DB_PATH = "wildlife_db"
COLLECTION_NAME = "kenya_wildlife_corpus"

EMBEDDING_MODEL = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# --- LLM SETUP ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0.1,
    google_api_key=os.getenv("GOOGLE_API_KEY")  
)

# --- 1. DEFINE THE RAG PROMPT TEMPLATE ---
# This template defines the agent's role and the required output structure.
RAG_PROMPT_TEMPLATE = """
**ROLE:** You are the Kenyan Wildlife Corridor Defense Agent, a highly specialized expert in Kenyan land law, ecological data, and historical land tenure.

**TASK:** Synthesize the provided context fragments into a professional, coherent, and evidence-based briefing document to answer the user's query.

**INSTRUCTIONS:**
1. **Strictly** use ONLY the provided context fragments below to answer the user's query.
2. Structure your response with clear, relevant headings based on the information available (e.g., **Legal Precedent/Status**, **Ecological Summary**, **Historical Context**, **Key Findings**, etc.).
3. Cite specific details from the context when making claims.
4. If the context does not contain sufficient information to answer the query, clearly state: "The requested information is not available in the current knowledge base."
5. Be concise but comprehensive. Focus on the most relevant information for the query.

--- CONTEXT FRAGMENTS ---
{context}

--- USER QUERY ---
{query}

--- BRIEFING DOCUMENT ---
"""

def create_retriever():
    """Loads the vector store and sets up the retriever for LangChain."""
    if not os.path.exists(CHROMA_DB_PATH):
        raise FileNotFoundError(
            f"Vector database not found at '{CHROMA_DB_PATH}'. Please ensure you ran the indexing script first!"
        )

    # 1. Load the existing Chroma database from disk
    db = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=EMBEDDING_MODEL,
        collection_name=COLLECTION_NAME
    )
    
    # 2. Convert the database into a retriever object for use in the RAG chain
    return db.as_retriever(search_kwargs={"k": 4})

def run_rag_chain(user_query: str):
    """Executes the complete Retrieval-Augmented Generation pipeline."""
    retriever = create_retriever()
    
    # Create the prompt from the template
    rag_prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

    # Define the RAG Chain using LangChain Expression Language (LCEL)
    rag_chain = (
        # 1. RETRIEVAL: Retrieve context chunks
        {"context": retriever, "query": RunnablePassthrough()}
        # 2. PROMPT: Format the context and query into the instruction prompt
        | rag_prompt
        # 3. GENERATION: Pass the final prompt to the Gemini LLM
        | llm
        # 4. PARSING: Extract the string response
        | StrOutputParser()
    )

    print(f"\n--- Running Agent for Query: '{user_query}' ---\n")
    response = rag_chain.invoke(user_query)
    
    return response

if __name__ == "__main__":
    print("\n" + "="*70)
    print("KENYAN WILDLIFE CORRIDOR DEFENSE AGENT")
    print("="*70)
    print("Ask questions about Kenyan land law, wildlife corridors, and ecology.")
    print("Type 'exit' or 'quit' to stop.\n")
    
    while True:
        user_query = input("Your Query: ").strip()
        
        if user_query.lower() in ['exit', 'quit', 'q']:
            print("\nAgent shutting down. Goodbye!")
            break
        
        if not user_query:
            print("Please enter a valid query.\n")
            continue
        
        try:
            briefing = run_rag_chain(user_query)
            
            print("\n" + "="*70)
            print("BRIEFING DOCUMENT")
            print("="*70)
            print(briefing)
            print("\n")
            
        except Exception as e:
            print(f"\nERROR: {e}\n")