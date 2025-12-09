import streamlit as st
from rag import process_urls, generate_answer

# Page configuration
st.set_page_config(
    page_title="Real Estate Assistant",
    page_icon="🏡",
    layout="wide"
)

# CSS to make it "One Page" (Remove top padding)
st.markdown("""
    <style>
        .block-container {
            padding-top: 3rem;
            padding-bottom: 0rem;
        }
        h1 {
            margin-bottom: 0px;
        }
    </style>
""", unsafe_allow_html=True)

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
    st.header("📝 Guide")
    st.markdown("""
    **Welcome!** This tool helps you analyze real estate articles quickly.
    
    1.  **Paste URLs** of articles.
    2.  Click **Process URLs**.
    3.  **Ask questions** to get insights.
    """)
    st.caption("Powered by Groq & LangChain")

# Main Title (Compact)
st.markdown("### 🏡 RAG-Based Real Estate Assistant")

# Main Layout: 2 Columns [1 (Narrow Config), 2.5 (Wide Results)]
# This width difference forces the answer text to be wider and thus shorter vertically
col_config, col_main = st.columns([1, 2.5], gap="medium")

# Left Column: Configuration
with col_config:
    st.markdown("**1. Configure Sources**")
    st.text_input(
        "URL 1", placeholder="https://example.com/article-1", key="url1", label_visibility="collapsed"
    )
    st.text_input(
        "URL 2", placeholder="https://example.com/article-2", key="url2", label_visibility="collapsed"
    )
    st.text_input(
        "URL 3", placeholder="https://example.com/article-3", key="url3", label_visibility="collapsed"
    )

    # Process Button with minimal spacing
    process_btn = st.button("🚀 Process URLs", type="primary", use_container_width=True)
    
    # Status Area (Visible Container)
    status_container = st.container()

# Right Column: Analysis
with col_main:
    # 2. Analysis Section - No Header to save space
    
    # If not processed, show a small hint
    if not st.session_state.urls_processed:
        st.info("👈 Add URLs and click **Process** to start.")
        
    else:
        # Chat Interface - Top Alignment
        col_q, col_btn = st.columns([4, 1])
        with col_q:
            question = st.text_input("Ask Question:", placeholder="e.g. key market trends?", label_visibility="collapsed")
        with col_btn:
            ask_btn = st.button("Generate Answer", type="secondary", use_container_width=True)
        
        if ask_btn or (question and process_btn): # Trigger if button clicked
             if question:
                with st.spinner("Analyzing..."):
                    try:
                        answer, sources = generate_answer(question)
                        
                        # Answer Display
                        st.markdown("#### 💡 Answer")
                        st.info(answer) # Info box is clean and compact
                        
                        # Sources in expander to save huge vertical space
                        with st.expander("View Sources"):
                            st.caption(sources)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
             else:
                st.warning("Please enter a question.")

# Logic for Processing
if process_btn:
    urls = [url for url in [st.session_state.url1, st.session_state.url2, st.session_state.url3] if url.strip()]
    
    if not urls:
        status_container.error("Please input a URL.")
    else:
        with status_container:
            # Expanded=True so user sees the "Processing" state immediately
            with st.status("Processing articles...", expanded=True) as status:
                try:
                    for log in process_urls(urls):
                        st.write(log)
                    st.session_state.urls_processed = True
                    status.update(label="✅ Ready! Ask questions on the right.", state="complete", expanded=False)
                    
                    # Explicit success message that persists slightly better than just the status label
                    st.success("Docs Processed! 👉 Go to 'Ask Question'")
                    
                    st.rerun()
                except Exception as e:
                    status.update(label="❌ Failed", state="error")
                    st.error(f"Error: {str(e)}")
