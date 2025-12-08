# 📚 RAG-Based Article Q&A Assistant

A powerful Streamlit application that uses Retrieval Augmented Generation (RAG) to answer questions based on content from articles you provide via URLs.

## 🌟 Features

- **3-Tab Interface**: Easily paste up to 3 article URLs in dedicated tabs
- **Intelligent Content Extraction**: Automatically extracts article content from various website structures
- **RAG-Powered Q&A**: Ask questions and get accurate answers based on article content
- **Source Attribution**: See which articles were used to generate answers
- **Beautiful UI**: Clean, modern interface with visual feedback and status indicators
- **Session Management**: Maintains state across interactions with reset functionality

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser (for Selenium web scraping)
- GROQ API Key (get one from https://console.groq.com)

### Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd "e:/1. Desktop Files/All AI ML Projects/Real Estate Assistant"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables**:
   - Make sure your `.env` file contains your GROQ API key:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     ```

### Running the Application

1. **Start the Streamlit app**:
   ```bash
   streamlit run main.py
   ```

2. **Access the application**:
   - The app will automatically open in your default browser
   - Or manually navigate to `http://localhost:8501`

## 📖 How to Use

### Step 1: Add Article URLs
1. Click on each of the 3 tabs: "Article 1", "Article 2", "Article 3"
2. Paste article URLs in the text input fields
3. You can add 1, 2, or all 3 URLs (at least 1 is required)

### Step 2: Process Articles
1. Click the **"🚀 Process URLs"** button
2. Wait while the system:
   - Fetches article content using a headless browser
   - Extracts and chunks the text
   - Creates vector embeddings
   - Stores everything in the database
3. You'll see real-time progress updates

### Step 3: Ask Questions
1. Once processing is complete, the question input will be enabled
2. Type your question in the text field
3. The AI will:
   - Search through the article content
   - Generate a comprehensive answer
   - Show you which sources were used

### Step 4: Reset (Optional)
- Use the **"🔄 Clear All & Reset"** button in the sidebar to start over

## 🛠️ Technical Architecture

### Components

- **main.py**: Streamlit UI with tab-based interface and session management
- **rag.py**: RAG pipeline including:
  - Web scraping with Selenium
  - Content extraction with BeautifulSoup
  - Text chunking with LangChain
  - Vector storage with ChromaDB
  - Question answering with GROQ LLM (Llama 3.3 70B)

### Technologies Used

- **Frontend**: Streamlit
- **LLM**: GROQ (Llama 3.3 70B Versatile)
- **Embeddings**: HuggingFace (sentence-transformers/all-MiniLM-L6-v2)
- **Vector Store**: ChromaDB
- **Web Scraping**: Selenium + BeautifulSoup4
- **Framework**: LangChain

## 🎯 Supported Article Types

The application uses intelligent content extraction that works with various article structures including:
- News websites
- Blog posts
- Documentation pages
- Medium articles
- And many more!

The system tries multiple extraction strategies to ensure maximum compatibility.

## 🔧 Configuration

You can modify the following constants in `rag.py`:

- `CHUNK_SIZE`: Size of text chunks (default: 1000)
- `EMBEDDING_MODEL`: HuggingFace model for embeddings
- `COLLECTION_NAME`: ChromaDB collection name
- LLM parameters (temperature, max_tokens)

## 📝 Example Use Cases

1. **Research**: Compare information across multiple articles
2. **Fact-checking**: Verify claims by asking questions
3. **Summarization**: Get key points from long articles
4. **Analysis**: Extract specific information from multiple sources

## ⚠️ Troubleshooting

### Issue: Chrome driver not found
**Solution**: The app automatically downloads the Chrome driver on first run. Ensure you have Chrome installed.

### Issue: No content extracted
**Solution**: 
- Check if the URLs are accessible
- Some websites have bot protection
- Try different article URLs

### Issue: API errors
**Solution**: 
- Verify your GROQ API key in the `.env` file
- Check your internet connection
- Ensure you haven't exceeded API rate limits

## 📄 License

This project is for educational and research purposes.

## 🤝 Contributing

Feel free to fork, modify, and enhance this application for your needs!

---

**Built with ❤️ using Streamlit and LangChain**
