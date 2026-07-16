# AI Legal Document Assistant

An AI-powered conversational document assistant that allows users to upload PDF legal documents, index them, and hold interactive chat sessions. It leverages Retrieval-Augmented Generation (RAG) powered by Google Gemini Models (`gemini-2.5-flash` and `gemini-embedding-2`) and a Chroma vector database.

🌐 **Live Demo**: [Streamlit Live Link](https://ai-legal-document-assistant-behnsscuphkyj8nxxl4uju.streamlit.app/)

---

## 🚀 Features

* **Interactive Chat Interface**: A native Streamlit chat UI that displays full conversation history with custom role styling.
* **Conversational Memory**: Retains the context of prior messages in the active session to support follow-up questions.
* **Contextual Question Rewriting**: Uses a dedicated query-rewriter prompt with Gemini to translate conversational queries (e.g., resolving pronouns like "it", "this", or "that") into standalone search questions.
* **PDF Upload & Parsing**: Easily upload any PDF document directly through the Streamlit interface.
* **Intelligent Text Chunking**: Automatically processes, splits, and overlaps document text for optimal retrieval accuracy using LangChain splitters.
* **Vector Search & Indexing**: Uses Chroma DB to store and search text chunk embeddings.
* **Maximal Marginal Relevance (MMR) Retrieval**: Fetches the most relevant yet diverse context chunks to provide comprehensive answers.
* **Context-Bound Question Answering**: Instructs Google Gemini to answer questions *strictly* using the provided context, ensuring trust and minimizing hallucinations.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend UI** | [Streamlit](https://streamlit.io/) | Lightweight web framework for building interactive UI |
| **Orchestration** | [LangChain](https://www.langchain.com/) | Framework for building LLM-powered applications |
| **LLM Model** | [gemini-2.5-flash](https://ai.google.dev/) | Multimodal model optimized for speed, reasoning, and QA |
| **Embeddings** | [gemini-embedding-2](https://ai.google.dev/) | Generating vector representations of text segments |
| **Vector DB** | [Chroma](https://www.trychroma.com/) | Light, open-source embedded vector database |
| **PDF Parser** | [PyPDF](https://pypdf.readthedocs.io/) | Python library for reading PDF documents |

---

## 📁 Directory Structure

```text
AI Legal Document Assistant/
├── backend/
│   ├── loader_splitter.py  # Loads PDF documents and splits text into chunks
│   ├── rag.py              # Prompt templates (rewriter & QA), retriever, and conversational QA logic
│   └── vector_store.py     # Embeddings initialization and vector database creation
├── data/
│   └── doc.pdf             # Sample directory with a PDF document
├── app.py                  # Main Streamlit application entrypoint
├── requirements.txt        # Python package dependencies
├── .env                    # System environment variables (e.g. GEMINI_API_KEY)
└── .gitignore              # Files excluded from git tracking
```

---

## ⚙️ How it Works

The system implements the **Retrieval-Augmented Generation (RAG)** pipeline as shown below:

1. **Document Ingestion**: The PDF document is parsed into text pages.
2. **Text Chunking**: Pages are broken down into chunks of `1000` characters with a `200` character overlap to maintain semantic continuity.
3. **Vectorization**: Chunks are processed by Google's `gemini-embedding-2` model to produce dense vector representations.
4. **Conversational Contextualization & Query Rewriting**: When a follow-up query is entered, the session's chat history is compiled. Google Gemini (`gemini-2.5-flash`) rewrites the latest query into a standalone question to resolve references and pronouns (e.g. turning "What is its termination clause?" into "What is the termination clause of the lease agreement?").
5. **Retrieval**: Chroma DB retrieves relevant document segments using **MMR (Maximal Marginal Relevance)**, prioritizing both relevance and diversity to extract the top 3 segments.
6. **Contextual & Bound QA**: The retrieved segments and conversational history are fed as context to `gemini-2.5-flash`. The model responds strictly based on the provided context or states if the info is unavailable.

---

## ⚡ Setup & Installation

### 1. Prerequisites
Ensure you have Python 3.10+ installed.

### 2. Clone the Repository
Clone or download the project files into your local directory.

### 3. Create a Virtual Environment
Create and activate a python virtual environment:

**On Windows (Command Prompt/PowerShell):**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
Install all package requirements:
```bash
pip install -r requirements.txt
```

### 5. Environment Configuration
Create a `.env` file in the root directory of the project and specify your Google Gemini API Key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 🖥️ Running the Application

Start the Streamlit application server:
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser. Upload your legal PDF document, wait for the processing to finish, and start querying your document!
