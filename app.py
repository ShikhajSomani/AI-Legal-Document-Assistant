import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.loader_splitter import load_pdf
from backend.loader_splitter import split_document
from backend.vector_store import get_embeddings
from backend.vector_store import create_vectors
from backend.rag import create_retriever
from backend.rag import ask_question

load_dotenv()

st.title("AI Legal Document Assistant")

gemini_api = os.getenv('GEMINI_API_KEY')

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=gemini_api,
    temperature=0
)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader(
    "Upload the pdf",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_file:

    all_docs = []

    for file in uploaded_file:
        temppdf = f"./temp.pdf"
        with open(temppdf, "wb") as f:
            f.write(file.getvalue())
            f_name = file.name

        docs = load_pdf(temppdf)
        final_docs = split_document(docs)
        all_docs.extend(final_docs)

    embeddings = get_embeddings()
    create_vectors(all_docs, embeddings)

    st.session_state.current_file = f_name
    st.success("Document processed successfully!")

if "vector_store" in st.session_state:
    retriever = create_retriever()

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask any question related to the uploaded document?")

    if question:
        st.session_state.chat_history.append(
            {
                "role":"user",
                "content":question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = ask_question(question, retriever, llm, st.session_state.chat_history)
                st.markdown(response)

        st.session_state.chat_history.append(
            {
            "role":"assistant",
            "content":response
            }
        )