import streamlit as st
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv

load_dotenv()

gemini_api = os.getenv('GEMINI_API_KEY')

st.title("AI Legal Document Assistant")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=gemini_api,
    temperature=0
)

file = "C:\\Users\\Shikhaj Somani\\OneDrive\\Desktop\\GenAI\\AI Legal Document Assistant\\data\\doc.pdf"

if file:
    pdf_reader = PyPDFLoader(file)
    docs = pdf_reader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    final_documents = text_splitter.split_documents(docs)
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2",
        google_api_key=gemini_api
    )
    
    vectors = Chroma.from_documents(
        documents=final_documents,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    st.success("Vectors created successfully!")
    
    retriever = vectors.as_retriever(
        search_type="similarity",
        search_kwargs={"k":4}
    )

    prompt = ChatPromptTemplate.from_template(
        """
        You are an helpful AI assistant
        Answer the user's question ONLY using the context provided.
        <context>
        {context}
        </context>

        Question:
        {question}

        If the answer is not found in the context, then reply:
        "I couldn't find the information in the uploaded document"

        Give clear and concise answers.
        """
    )

    question = st.text_input("Ask any question related to the uploaded document?")

    if question:
        retrieved_docs = retriever.invoke(question)

        context = "\n\n".join(
            doc.page_content
            for doc in retrieved_docs
        )

        formatted_prompt = prompt.format(
            context=context,
            question=question
        )

        response = llm.invoke(formatted_prompt)

        st.subheader("Answer:")
        st.write(response.content)