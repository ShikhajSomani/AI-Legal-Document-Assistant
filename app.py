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

gemini_api = st.text_input("Enter your api key", type="password")

if gemini_api:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=gemini_api,
        temperature=0
    )

    uploaded_file = st.file_uploader(
        "Upload the pdf",
        type=["pdf"]
    )

    if uploaded_file:
        if "current_file" not in st.session_state or st.session_state.current_file != uploaded_file.name:

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
                temp.write(uploaded_file.read())
                file = temp.name

            docs = load_pdf(file)
            final_docs = split_document(docs)
            embeddings = get_embeddings()
            create_vectors(final_docs, embeddings)

            st.session_state.current_file = uploaded_file.name
            st.success("Document processed successfully!")

    if "vector_store" in st.session_state:
        retriever = create_retriever()

        question = st.text_input("Ask any question related to the uploaded document?")

        if question:
            st.subheader("Answer:")
            with st.spinner("Thinking..."):
                response = ask_question(question, retriever, llm)
            st.write(response)