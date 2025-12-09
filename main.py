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
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Title and Description
st.title("📚 RAG-Based Article Q&A Assistant")
st.markdown("""
Welcome! This tool allows you to:
1. **Paste article URLs** below
2. **Process the articles** to extract their content
3. **Ask questions** and get answers based on the article content
""")

st.divider()

# URL Inputs - Vertical Layout matches user request
st.subheader("🔗 Article URLs")
st.caption("Paste your article links below:")

col_input, col_void = st.columns([2, 1])

with col_input:
    st.session_state.url1 = st.text_input(
        "Article 1 URL",
        value=st.session_state.url1,
        placeholder="https://example.com/article-1",
        key="input_url1"
    )

    st.session_state.url2 = st.text_input(
        "Article 2 URL",
        value=st.session_state.url2,
        placeholder="https://example.com/article-2",
        key="input_url2"
    )

    st.session_state.url3 = st.text_input(
        "Article 3 URL",
        value=st.session_state.url3,
        placeholder="https://example.com/article-3",
        key="input_url3"
    )

st.divider()

# Process URLs section
st.subheader("📥 Process Articles")

# Collect valid URLs
urls = [url for url in [st.session_state.url1, st.session_state.url2, st.session_state.url3] if url.strip()]

col_act, col_info = st.columns([1, 2])

with col_act:
    process_button = st.button("🚀 Process URLs", type="primary", use_container_width=True)

with col_info:
    if urls:
        st.info(f"Ready to process {len(urls)} URL(s).")
    else:
        st.warning("Please add at least one URL above.")

# Status display
status_placeholder = st.empty()

if process_button:
    if not urls:
        status_placeholder.error("❌ Please provide at least one URL.")
    else:
        with status_placeholder.container():
            st.info(f"Processing {len(urls)} article(s)... Please wait.")
            progress_text = st.empty()
            
            try:
                # No manual API key passed; relies on rag.py's internal fallback
                for status in process_urls(urls):
                    progress_text.markdown(f"**Status:** {status}")
                
                st.session_state.urls_processed = True
                status_placeholder.success("✅ All articles processed successfully! You can now ask questions below.")
            except Exception as e:
                st.session_state.urls_processed = False
                status_placeholder.error(f"❌ An error occurred: {str(e)}")

st.divider()

# Q&A Section - Only visible after processing
if st.session_state.urls_processed:
    st.header("💬 Ask Questions")
    
    # Input for question
    question = st.text_input("Type your question here:", placeholder="What are the main takeaways?")
    
    if st.button("Get Answer", type="primary") and question:
        with st.spinner("Generating answer..."):
            try:
                answer, sources = generate_answer(question)
                
                st.markdown("### 🤖 Answer")
                st.write(answer)
                
                with st.expander("📚 Sources / References"):
                    st.write(sources)
                    
            except Exception as e:
                st.error(f"Error generating answer: {str(e)}")
elif not urls:
    st.caption("Add URLs and click Process to start asking questions.")
