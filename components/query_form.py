import streamlit as st

def on_example_click(question):
    st.session_state["query_input"] = question
    st.experimental_rerun()
    
def set_query_input(question_text):
    # This function is executed when an example button is clicked.
    st.session_state["query_input"] = question_text
    # Note: State change alone triggers the necessary rerun.

def display_query_form():
    """
    Displays the main query input form and submit button,
    using session_state to pre-fill the input.
    """
    current_value = st.session_state.get("query_input", "")

    query = st.text_area(
        label="Enter your question about Kenyan wildlife:",
        key="query_input",
        height=120,
        placeholder="Example: Tell me about lion prides in Kenya, or how do elephants communicate?",
        help="Ask anything about wildlife, conservation, or the Maasai Mara!"
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        submit = st.button("🔎 Ask Akoth", key="submit_btn", use_container_width=True)

    return query, submit

def display_examples():
    st.markdown("### 💡 Example Questions")
    
    example_questions = [
        ("🦁", "Tell me about lion prides and their behavior in Kenya."),
        ("🐘", "How do wildebeests know when to migrate?"),
        ("🌍", "What conservation efforts protect Kenyan wildlife?"),
        ("🦒", "What's unique about giraffe ecology in the savanna?"),
    ]
    
    for emoji, question in example_questions:
        col1, col2 = st.columns([0.5, 9.5]) 
        
        with col1:
            st.markdown(emoji)
        
        with col2:
            # Use on_click to set the state cleanly BEFORE the rerun
            st.button(
                question, 
                key=f"example_{question}", 
                use_container_width=True,
                on_click=set_query_input,  # The callback function
                args=(question,)           # The argument to pass to the callback
            )

    st.divider()
    st.caption("Built with **Streamlit** • **LangChain** • **ChromaDB** • Powered by **Akoth** 🦁")
