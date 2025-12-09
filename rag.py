import os
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

load_dotenv()

# Constants
import tempfile
import shutil

CHUNK_SIZE = 1000
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# Use a temporary directory for the vector store to avoid Read-Only errors on Cloud
# We create a specific subdirectory 'rag_vectorstore' in the system temp location
VECTORSTORE_DIR = Path(tempfile.gettempdir()) / "rag_vectorstore"
COLLECTION_NAME = "articles"


VECTORSTORE_DIR = Path(tempfile.gettempdir()) / "rag_vectorstore"
COLLECTION_NAME = "articles"

llm = None
vector_store = None


def initialize_components(api_key=None):
    """Initializes the LLM and Vector Store."""
    global llm, vector_store

    if llm is None:
        # 1. Try argument provided from UI (manual entry)
        final_api_key = api_key
        
        # 2. If not provided, try Streamlit Secrets (preferred automated method)
        if not final_api_key:
            try:
                if "GROQ_API_KEY" in st.secrets.get("general", st.secrets):
                     # Handle both [general] section or direct key
                     # depending on how secrets.toml is structured/read
                     final_api_key = st.secrets.get("GROQ_API_KEY") or st.secrets["general"].get("GROQ_API_KEY")
            except Exception:
                pass
        
        # 3. If still not found, try Environment Variable (local dev fallback)
        if not final_api_key:
            final_api_key = os.getenv("GROQ_API_KEY")

        if not final_api_key:
            st.error("❌ GROQ_API_KEY not found! Please set it in .streamlit/secrets.toml")
            st.stop()
            
        # Set env var for libraries that need it
        os.environ["GROQ_API_KEY"] = final_api_key
            
        llm = ChatGroq(
            api_key=final_api_key,
            model="llama-3.3-70b-versatile", 
            temperature=0.7, 
            max_tokens=1000
        )


    if vector_store is None:
        ef = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"trust_remote_code": True}
        )

        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=ef,
            persist_directory=str(VECTORSTORE_DIR)
        )


def extract_article_content(soup, url):
    """
    Extracts article content from various common HTML structures.
    Returns the extracted text or None if extraction fails.
    """
    # List of common article container selectors
    selectors = [
        # Class-based selectors
        ('div', 'ArticleBody-wrapper'),
        ('div', 'article-body'),
        ('div', 'post-content'),
        ('div', 'entry-content'),
        ('div', 'article-content'),
        ('article', None),
        ('div', 'content'),
        ('main', None),
        # ID-based selectors
    ]
    
    # Try class-based selectors first
    for tag, class_name in selectors:
        if class_name:
            element = soup.find(tag, class_=class_name)
        else:
            element = soup.find(tag)
        
        if element:
            text = element.get_text(separator=' ', strip=True)
            if len(text.strip()) > 200:
                return text
    
    # Try finding by ID
    for id_name in ['article', 'content', 'main-content', 'post']:
        element = soup.find(id=id_name)
        if element:
            text = element.get_text(separator=' ', strip=True)
            if len(text.strip()) > 200:
                return text
    
    # Fallback: get all paragraph text
    paragraphs = soup.find_all('p')
    if paragraphs:
        text = ' '.join([p.get_text(strip=True) for p in paragraphs])
        if len(text.strip()) > 200:
            return text
    
    return None


def process_urls(urls, api_key=None):
    """Processes URLs by automating a real browser and provides full diagnostics."""
    initialize_components(api_key=api_key)
    yield "🔄 Resetting vector store..."
    vector_store.reset_collection()

    all_docs = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    # Check if running on Streamlit Cloud (Linux) to set binary location
    # Streamlit Cloud usually installs chromium at /usr/bin/chromium
    if os.path.exists("/usr/bin/chromium"):
        chrome_options.binary_location = "/usr/bin/chromium"
    elif os.path.exists("/usr/bin/chromium-browser"):
        chrome_options.binary_location = "/usr/bin/chromium-browser"
    
    # Driver Handling:
    # On Streamlit Cloud (Linux), use the installed chromium-driver which matches the installed chromium version.
    # On Local (Windows/Mac), use ChromeDriverManager to download the correct driver.
    if os.path.exists("/usr/bin/chromedriver"):
        service = Service("/usr/bin/chromedriver")
    else:
        service = Service(ChromeDriverManager().install())
        
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        for idx, url in enumerate(urls, 1):
            yield f"📄 Processing Article {idx}/{len(urls)}: {url}"
            try:
                driver.get(url)
                time.sleep(5)  # Wait for page to load

                page_title = driver.title
                yield f"✅ Page loaded: '{page_title}'"

                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')

                # Extract article content using flexible selectors
                article_text = extract_article_content(soup, url)

                if article_text:
                    preview = article_text[:200].replace('\n', ' ')
                    yield f"✅ Content extracted ({len(article_text)} chars): {preview}..."
                    
                    doc = Document(
                        page_content=article_text, 
                        metadata={
                            "source": url,
                            "title": page_title
                        }
                    )
                    all_docs.append(doc)
                    yield f"✅ Article {idx} successfully processed!"
                else:
                    yield f"⚠️ Could not extract meaningful content from Article {idx}"
                    
            except Exception as e:
                yield f"❌ Error processing Article {idx}: {str(e)}"
                
            yield "─" * 50
            
    finally:
        driver.quit()

    if not all_docs:
        yield "❌ No content was extracted from any URL. Please check the URLs and try again."
        return

    yield f"📝 Splitting {len(all_docs)} article(s) into chunks..."
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=200
    )
    docs = text_splitter.split_documents(all_docs)

    yield f"💾 Adding {len(docs)} chunks to vector database..."
    uuids = [str(uuid.uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(docs, ids=uuids)
    yield "✅ Complete! Vector database is ready for questions."


def generate_answer(query):
    """Generates an answer to a query using the RAG system."""
    if not vector_store:
        raise RuntimeError("Vector database is not initialized. Please process URLs first.")

    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    template = """You are a helpful assistant that answers questions based on the provided article content.

Use the following pieces of context from the articles to answer the question at the end.
If you don't know the answer based on the context, just say that you don't have enough information to answer. 
Do not make up information that is not in the context.

IMPORTANT: Provide a DIRECT and CONCISE answer. Do not start with "According to the context" or "Based on the articles". Just give the answer directly.
If the answer is a specific number, date, or fact, provide just that with minimal context.

Context from articles:
{context}

Question: {question}

Helpful Answer:"""
    
    prompt = PromptTemplate.from_template(template)

    rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
    )

    answer = rag_chain.invoke(query)

    # Get source documents
    docs = retriever.invoke(query)
    sources = set()
    for doc in docs:
        if 'source' in doc.metadata:
            sources.add(doc.metadata['source'])

    sources_str = "\n".join(list(sources))

    return answer.content, sources_str