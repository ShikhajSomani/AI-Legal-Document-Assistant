# AI Legal Document Assistant

An AI-powered document assistant that allows users to upload PDF legal documents, index them, and ask questions. It uses Retrieval-Augmented Generation (RAG) powered by Google Gemini Models (`gemini-2.5-flash` and `gemini-embedding-2`) and a Chroma vector database.

🌐 **Live Demo**: [Streamlit Live Link](https://ai-legal-document-assistant-behnsscuphkyj8nxxl4uju.streamlit.app/)

---

## 🚀 Features

*   **PDF Upload & Parsing**: Easily upload any PDF document directly through the Streamlit interface.
*   **Intelligent Text Chunking**: Automatically processes, splits, and overlaps document text for optimal retrieval accuracy.
*   **Vector Search & Indexing**: Uses Chroma DB to store and search text chunk embeddings.
*   **Maximal Marginal Relevance (MMR) Retrieval**: Fetches the most relevant, diverse context chunks to provide comprehensive answers.
*   **Context-Bound Question Answering**: Instructs Google Gemini to answer questions *strictly* using the uploaded context, ensuring trust and minimizing hallucinations.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend UI** | [Streamlit](https://streamlit.io/) | Lightweight web framework for building interactive UI |
| **Orchestration** | [LangChain](https://www.langchain.com/) | Framework for building LLM-powered applications |
| **LLM Model** | [gemini-2.5-flash](https://ai.google.dev/) | Multimodal model optimized for speed and QA |
| **Embeddings** | [gemini-embedding-2](https://ai.google.dev/) | Generating vector representations of text segments |
| **Vector DB** | [Chroma](https://www.trychroma.com/) | Light, open-source embedded vector database |
| **PDF Parser** | [PyPDF](https://pypdf.readthedocs.io/) | Python library for reading PDF documents |

---

## 📁 Directory Structure

```text
AI Legal Document Assistant/
├── backend/
│   ├── loader_splitter.py  # Loads PDF documents and splits text into chunks
│   ├── rag.py              # Defines the prompt template, retriever, and QA logic
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
4. **Retrieval**: When a query is made, Chroma DB queries the vectors using **MMR (Maximal Marginal Relevance)**, prioritizing both relevance and diversity to extract the top 3 segments.
5. **Contextual QA**: The retrieved segments are fed as context to `gemini-2.5-flash`. The model responds strictly based on the provided context or states if the info is unavailable.

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
