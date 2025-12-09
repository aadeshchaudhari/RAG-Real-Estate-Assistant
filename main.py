import streamlit as st
from rag import process_urls, generate_answer

# Page configuration
st.set_page_config(
    page_title="Real Estate Assistant",
    page_icon="🏡",
    layout="wide"
)

# Initialize session state
if 'urls_processed' not in st.session_state:
    st.session_state.urls_processed = False
if 'url1' not in st.session_state:
    st.session_state.url1 = ""
if 'url2' not in st.session_state:
    st.session_state.url2 = ""
if 'url3' not in st.session_state:
    st.session_state.url3 = ""

# Sidebar - Instructions & About
with st.sidebar:
    st.header("� Guide")
    st.markdown("""
    **Welcome!** This tool helps you analyze real estate articles quickly.
    
    **How to use:**
    1.  **Paste URLs** of articles in the configuration panel.
    2.  Click **Process URLs** to extract content.
    3.  **Ask questions** in the chat panel to get specific insights.
    """)
    
    st.divider()
    with st.expander("ℹ️ About"):
        st.markdown("""
        **RAG-Based Real Estate Assistant**
        
        Powered by:
        - Groq (Llama 3.3)
        - LangChain
        - ChromaDB
        """)

# Main Title
st.title("🏡 RAG-Based Real Estate Assistant")
st.caption("AI-Powered Research & Analysis Tool")

st.divider()

# Main Layout: 2 Columns
col_config, col_main = st.columns([1, 1.5], gap="large")

# Left Column: Configuration
with col_config:
    st.subheader("⚙️ Configuration")
    
    st.markdown("**Article Sources**")
    st.text_input(
        "Article 1",
        placeholder="https://example.com/article-1",
        key="url1",
        label_visibility="collapsed"
    )
    st.text_input(
        "Article 2",
        placeholder="https://example.com/article-2",
        key="url2",
        label_visibility="collapsed"
    )
    st.text_input(
        "Article 3",
        placeholder="https://example.com/article-3",
        key="url3",
        label_visibility="collapsed"
    )

    st.markdown("---")
    
    # Process Button
    process_btn = st.button("🚀 Process URLs", type="primary", use_container_width=True)
    
    # Status Area (Compact)
    status_container = st.container()
    
# Right Column: Analysis
with col_main:
    st.subheader("🤖 Analysis & Insights")
    
    # Placeholder for when no content is processed
    if not st.session_state.urls_processed:
        st.info("👈 Please add URLs and click **Process** in the configuration panel to start.")
        
    else:
        # Chat Interface
        question = st.text_input("Ask a question about the articles:", placeholder="e.g., What are the key market trends mentioned?")
        
        if st.button("Generate Answer", type="secondary"):
            if question:
                with st.spinner("Analyzing content..."):
                    try:
                        answer, sources = generate_answer(question)
                        
                        st.markdown("#### 💡 Answer")
                        st.info(answer)
                        
                        with st.expander("📚 View Referenced Sources"):
                            st.text(sources)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter a question.")

# Logic for Processing (Handling in main flow to update UI)
if process_btn:
    urls = [url for url in [st.session_state.url1, st.session_state.url2, st.session_state.url3] if url.strip()]
    
    if not urls:
        status_container.error("❌ Please input at least one URL.")
    else:
        with status_container:
            with st.status("🔄 Processing articles...", expanded=True) as status:
                st.write("Initializing RAG engine...")
                try:
                    for log in process_urls(urls):
                        st.text(log) # Show logs concisely
                        
                    st.session_state.urls_processed = True
                    status.update(label="✅ Ready! Ask questions on the right.", state="complete", expanded=False)
                    st.rerun() # Rerun to update the right column state
                except Exception as e:
                    status.update(label="❌ Failed", state="error")
                    st.error(f"Error: {str(e)}")
                    st.session_state.urls_processed = False
