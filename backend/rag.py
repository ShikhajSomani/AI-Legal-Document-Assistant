import streamlit as st
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    """
    You are an AI Legal Assistant specializing in legal document analysis.

    Use ONLY the provided context to answer the user's question.

    Guidelines:
    1. Do not use external knowledge.
    2. If the answer is unavailable, reply:
    "The uploaded document does not contain sufficient information to answer this question."
    3. Whenever possible, cite the relevant section, clause, article, or heading.
    4. If the question asks for an explanation, simplify the legal language while preserving its original meaning.
    5. Do not offer legal opinions, recommendations, or advice.
    6. Be factual, concise, and accurate.

    <context>
    {context}
    </context>

    Question:
    {question}
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