import streamlit as st
from langchain_core.prompts import ChatPromptTemplate

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

def create_retriever():
    return st.session_state.vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k":3}
    )

def ask_question(question, retriever, llm):
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

    return response.content