# 🦁 Akoth: : Maasai Mara Wildlife Expert 

Meet **Akoth**, your friendly AI wildlife expert for the Maasai Mara and Kenyan wildlife! Powered by Streamlit, LangChain, Google Gemini AI models, and ChromaDB vector search. Akoth provides engaging, conversational insights about Kenyan wildlife, Maasai Mara ecosystems, and conservation efforts using a retrieval-augmented generation (RAG) method..

## 🌟 Features

- **Smart Document Retrieval**: Semantic search across Kenyan wildlife conservation PDFs and texts
- **Embedding-Based Search**: HuggingFace Sentence Transformers for intelligent similarity matching
- **Interactive Web Interface**: Clean, intuitive Streamlit UI with warm brown & green theme
- **RAG Pipeline**: Combines document retrieval with LLM responses for accurate answers
- **Expert Knowledge**: Powered by Akoth's deep understanding of Maasai Mara and Kenyan wildlife
- **Modular Architecture**: Separate indexing and querying scripts for flexibility

## 💡 How It Works

1. **Indexing Phase** (`index.py`):
   - Reads documents from `docs/` folder
   - Creates embeddings using HuggingFace Sentence Transformers
   - Stores vectors in Chroma vector database

2. **Query Phase** (`app.py`):
   - User enters a natural language question
   - System retrieves relevant documents using semantic similarity
   - Google Generative AI (Gemini) generates expert response based on context
   - Response displayed in styled response card

3. **Retrieval-Augmented Generation (RAG)**:
   - Documents are split into chunks
   - Chunks are embedded and stored in vector DB
   - On query, relevant chunks are retrieved
   - Retrieved context is passed to LLM for answer generation


## Installation and Setup

1. Create and activate a Python virtual environment:
python -m venv venv
source venv/bin/activate

2. Install required dependencies using the provided requirements.txt file:
pip install -r requirements.txt

## Usage

1. To build the document index, run:
python index.py

2. To start the Streamlit app for querying:
streamlit run app.py

## Notes

- The `langchain-huggingface` package should be imported as:
from langchain_huggingface import HuggingFaceEmbeddings

- Make sure your PDF or text documents related to Kenyan wildlife conservation are placed in the appropriate data directory for indexing.

## Project Structure

- `index.py`: Script to build the vector index over conservation documents.
- `app.py`: Streamlit app to interface with the RAG agent.
- `docs/`: Folder containing the conservation PDFs and texts.
- `requirements.txt`: List of all Python dependencies.
- `venv/`: Python virtual environment folder.

## References

- National Wildlife Strategy 2030 - Kenya
- Kenya Wildlife Service Strategic Plans
- African Wildlife Foundation Kenya Conservation Reports

## License

This project is open source and available under the MIT License.

