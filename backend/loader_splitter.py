import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import streamlit as st

def load_pdf(file):
    if file:
        pdf_reader = PyPDFLoader(file)
        docs = pdf_reader.load()
        return docs
    else:
        return "No file path found."

def split_document(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200 
    )
    final_docs = text_splitter.split_documents(docs)
    return final_docs