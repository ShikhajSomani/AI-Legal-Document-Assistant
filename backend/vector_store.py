import os
import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

gemini_api = os.getenv('GEMINI_API_KEY')

def get_embeddings():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2",
        google_api_key=gemini_api
    )
    return embeddings

def create_vectors(documents,embeddings):
    vectors = Chroma.from_documents(
        documents=documents,
        embedding=embeddings
    )
    
    st.session_state.vector_store = vectors
    return st.session_state.vector_store

