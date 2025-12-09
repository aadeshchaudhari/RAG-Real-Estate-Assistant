# 🏡 Real Estate RAG Assistant

**An AI-powered research tool that turns messy real estate articles into clear, actionable insights.**

---

## 💡 The Problem
Real estate research involves reading dozens of long, complex articles to find a few key stats or trends. Keeping track of interest rates, housing supply figures, and regional forecasts across multiple tabs is overwhelming and inefficient.

## 🚀 The Solution
I built this **Real Estate RAG Assistant** to automate that process. 

Instead of reading everything manually, you simply paste URLs into the dashboard. The app uses a **RAG (Retrieval-Augmented Generation)** engine to read the content for you, understand the context, and answer your specific questions instantly (e.g., *"What is the consensus on mortgage rates for 2025?"*).

It allows for **data-driven decision making** without the information overload.

---

## 🛠️ Tech Stack
This project utilizes a modern AI stack focused on speed and accuracy:

*   **LLM Engine**: [Groq](https://groq.com) (Llama 3 70B) for lightning-fast inference.
*   **Orchestration**: [LangChain](https://www.langchain.com) for managing the RAG pipeline.
*   **Vector Database**: [ChromaDB](https://www.trychroma.com) for semantic search and efficient context retrieval.
*   **Frontend**: [Streamlit](https://streamlit.io) for a clean, single-page dashboard UI.
*   **Data Ingestion**: BeautifulSoup & Selenium to handle diverse web content.

---

## ⚡ Key Features
*   **Multi-Source Analysis**: Intake up to 3 different article URLs simultaneously to cross-reference data.
*   **Context-Aware**: The AI doesn't hallucinate; it answers *strictly* based on the provided text, ensuring accuracy.
*   **Source Citation**: Every answer includes a reference list, so you know exactly where the data came from.
*   **Professional Dashboard**: A compact, single-view UI designed for quick side-by-side analysis.

---

## 🏃‍♂️ How to Run Locally

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/aadeshchaudhari/RAG-Real-Estate-Assistant.git
    cd RAG-Real-Estate-Assistant
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**
    ```bash
    streamlit run main.py
    ```

*Note: The app comes with a pre-configured embedded key for demonstration purposes, but for production use, it is recommended to add your own `GROQ_API_KEY` to `.streamlit/secrets.toml`.*

---

## 🔮 Future Improvements
*   **PDF Support**: Adding the ability to upload market reports directly.
*   **Chart Generation**: Visualizing extracted data points (e.g., interest rate trends) automatically.
*   **History**: Saving past conversations for reference.

---

**Author**: Aadesh Chaudhari
*Built with ❤️ to simplify complex research.*
