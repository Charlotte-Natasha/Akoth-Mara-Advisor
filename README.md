# Akoth: Maasai Mara Wildlife Expert 

Welcome to **Akoth**, an interactive Q&A app powered by Streamlit, LangChain, Google Gemini AI models, and ChromaDB vector search. Akoth provides engaging, conversational insights about Kenyan wildlife, Maasai Mara ecosystems, and conservation efforts using a retrieval-augmented generation (RAG) method.

## Features

- Natural language querying of a curated wildlife knowledge base
- Advanced LLM (Gemini) from Google GenAI used via LangChain SDK
- Contextual retrieval from ChromaDB vector store of wildlife documents
- User-friendly Streamlit interface with clickable example questions
- Easy setup with environment variable API keys and reusable Python modules

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

