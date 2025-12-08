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

# Status display
status_placeholder = st.empty()

if process_button:
    if not urls:
        status_placeholder.error("❌ Please provide at least one URL in the tabs above.")
    else:
        with status_placeholder.container():
            st.info(f"Processing {len(urls)} article(s)... Please wait.")
            progress_text = st.empty()
            
            for status in process_urls(urls):
                progress_text.markdown(f"**Status:** {status}")
            
            st.session_state.urls_processed = True
            st.success("✅ All articles processed successfully! You can now ask questions below.")

st.divider()

# Question answering section
st.subheader("💬 Ask Questions")

if not st.session_state.urls_processed:
    st.info("ℹ️ Please process the URLs first before asking questions.")

query = st.text_input(
    "Enter your question about the articles:",
    placeholder="What is the main topic discussed in these articles?",
    disabled=not st.session_state.urls_processed
)

if query and st.session_state.urls_processed:
    with st.spinner('🔍 Searching articles and generating answer...'):
        try:
            answer, sources = generate_answer(query)
            
            # Display answer in a nice card
            st.markdown("### 📝 Answer:")
            st.info(answer)
            
            # Display sources
            if sources:
                with st.expander("📚 View Sources", expanded=False):
                    st.markdown("**References:**")
                    for idx, source in enumerate(sources.split('\n'), 1):
                        if source.strip():
                            st.markdown(f"{idx}. [{source}]({source})")
        except RuntimeError as e:
            st.error(f"❌ Error: {str(e)}")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")

# Sidebar with instructions
with st.sidebar:
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