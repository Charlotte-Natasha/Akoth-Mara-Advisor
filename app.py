import streamlit as st
from dotenv import load_dotenv

# Import your custom components
from components.header import display_header
from components.query_form import display_query_form, display_examples

# Load environment variables
load_dotenv()

def load_css():
    """Load external CSS for styling."""
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    # Load CSS styles
    load_css()

    # Page config
    st.set_page_config(
        page_title="Akoth: Maasai Mara Wildlife Expert",
        page_icon="🦁",
        layout="wide"
    )

    # --- Sidebar ---
    with st.sidebar:
        st.header("About Akoth")
        st.info("""
        🌿 **Akoth** is a traditional Luo name meaning *'born at dawn'*.
        Just like the dawn brings light to the savanna, Akoth illuminates knowledge
        about the Maasai Mara, its wildlife, and conservation efforts.  

        This agent uses **RAG (Retrieval-Augmented Generation)** to provide accurate,
        engaging, and fun insights into Kenyan wildlife, ecosystems, and safari experiences.
        🦁🦒🐘
        """)
        
    # Display header component
    display_header()

    # Layout: main query column and system info column
    col1, col2 = st.columns([2, 1], gap="large")

    with col2:
        st.markdown("### System Info")
        # Lazy import for retriever status
        try:
            from query_agent import create_retriever
            retriever = create_retriever()
            st.success("Vector DB: available")
            st.caption(f"Collection: {getattr(retriever, 'collection', {}).get('name', '') or 'unknown'}")
        except Exception as e:
            st.warning(f"Vector DB load issue: {e}")
            
        # Display example questions below query form
        st.markdown("---")
        display_examples()

    with col1:
        # Query form
        query, submit = display_query_form()

        # Populate query from example if set
        if "example" in st.session_state and not query:
            query = st.session_state.pop("example")

        if submit and not query:
            st.warning("Please enter a query.")
        elif submit and query:
            from query_agent import run_agent  # Using your Akoth query agent
            with st.spinner("Searching knowledge base..."):
                try:
                    response = run_agent(query)
                    # Display in styled response card
                    st.markdown('<div class="response-card">', unsafe_allow_html=True)
                    st.markdown("### Response")
                    if isinstance(response, (list, dict)):
                        st.json(response)
                    else:
                        st.markdown(response)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"An error occurred while running the agent: {e}")

if __name__ == "__main__":
    main()