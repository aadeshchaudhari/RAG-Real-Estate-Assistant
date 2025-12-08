import streamlit as st
from rag import process_urls, generate_answer

# Page configuration
st.set_page_config(
    page_title="RAG Article Q&A Assistant",
    page_icon="📚",
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

# Title and Description
st.title("📚 RAG-Based Article Q&A Assistant")
st.markdown("""
Welcome! This tool allows you to:
1. **Paste article URLs** in the tabs below
2. **Process the articles** to extract their content
3. **Ask questions** and get answers based on the article content
""")

st.divider()

# Create tabs for URL inputs
tab1, tab2, tab3 = st.tabs(["📄 Article 1", "📄 Article 2", "📄 Article 3"])

with tab1:
    st.subheader("Article 1 URL")
    st.session_state.url1 = st.text_input(
        "Paste your first article link here:",
        value=st.session_state.url1,
        key="input_url1",
        placeholder="https://example.com/article-1"
    )
    if st.session_state.url1:
        st.success(f"✅ URL 1 added: {st.session_state.url1[:50]}...")

with tab2:
    st.subheader("Article 2 URL")
    st.session_state.url2 = st.text_input(
        "Paste your second article link here:",
        value=st.session_state.url2,
        key="input_url2",
        placeholder="https://example.com/article-2"
    )
    if st.session_state.url2:
        st.success(f"✅ URL 2 added: {st.session_state.url2[:50]}...")

with tab3:
    st.subheader("Article 3 URL")
    st.session_state.url3 = st.text_input(
        "Paste your third article link here:",
        value=st.session_state.url3,
        key="input_url3",
        placeholder="https://example.com/article-3"
    )
    if st.session_state.url3:
        st.success(f"✅ URL 3 added: {st.session_state.url3[:50]}...")

st.divider()

# Process URLs section
st.subheader("📥 Process Articles")
col1, col2 = st.columns([3, 1])

with col1:
    urls = [url for url in [st.session_state.url1, st.session_state.url2, st.session_state.url3] if url.strip()]
    if urls:
        st.info(f"📌 You have {len(urls)} URL(s) ready to process")
    else:
        st.warning("⚠️ Please add at least one URL in the tabs above")

with col2:
    process_button = st.button("🚀 Process URLs", type="primary", use_container_width=True)

# Sidebar with configuration and instructions
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key Handling
    # 1. Init session state for key if not exists
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
        
    api_key = st.session_state.api_key
    
    # 2. Try Secrets first
    if "GROQ_API_KEY" in st.secrets:
        st.success("✅ API Key found in Secrets")
        api_key = st.secrets["GROQ_API_KEY"]
        st.session_state.api_key = api_key # Sync
    else:
        # 3. Manual Input with Session State
        input_key = st.text_input(
            "🔑 Enter Groq API Key:", 
            type="password", 
            placeholder="gsk_...",
            value=st.session_state.api_key,
            help="Enter your key once, it will be saved for this session."
        )
        if input_key:
            st.session_state.api_key = input_key
            api_key = input_key
            st.success("✅ API Key provided")
    
    st.divider()

    st.header("ℹ️ How to Use")
    st.markdown("""
    1. **Add URLs**: Click on each tab and paste article links
    2. **Process**: Click "Process URLs" button
    3. **Ask**: Type your question in the question box
    4. **Get Answers**: Receive AI-generated answers from the articles
    """)
    
    st.divider()
    
    st.header("📊 Status")
    if st.session_state.urls_processed:
        st.success("✅ System Ready")
        st.metric("Processed Articles", len(urls))
    else:
        st.warning("⏳ Waiting for articles")
    
    st.divider()
    
    # Clear button
    if st.button("🔄 Clear All & Reset", use_container_width=True):
        st.session_state.urls_processed = False
        st.session_state.url1 = ""
        st.session_state.url2 = ""
        st.session_state.url3 = ""
        st.rerun()

# Status display
status_placeholder = st.empty()

if process_button:
    if not urls:
        status_placeholder.error("❌ Please provide at least one URL in the tabs above.")
    elif not api_key:
        status_placeholder.error("❌ Please provide a Groq API Key in the sidebar.")
    else:
        with status_placeholder.container():
            st.info(f"Processing {len(urls)} article(s)... Please wait.")
            progress_text = st.empty()
            
            try:
                for status in process_urls(urls, api_key=api_key):
                    progress_text.markdown(f"**Status:** {status}")
                
                st.session_state.urls_processed = True
                st.success("✅ All articles processed successfully! You can now ask questions below.")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")