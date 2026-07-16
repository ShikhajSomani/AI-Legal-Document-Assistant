import streamlit as st
from langchain_core.prompts import ChatPromptTemplate

rewrite_prompt = ChatPromptTemplate.from_template(
    """
    You are an AI assistant that rewrites follow-up questions.

    Given the conversation history and the user's latest question,
    rewrite the latest question into a standalone question.

    Rules:
    - Do NOT answer the question.
    - Preserve the user's original intent.
    - Resolve pronouns like "it", "they", "this", and "that".
    - Return only the rewritten question.

    Conversation History:
    {chat_history}

    Latest Question:
    {question}
    """
)

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

    Conversation History:
    {chat_history}

    Context:
    {context}

    Question:
    {rewritten_question}
    """
)

def create_retriever():
    return st.session_state.vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k":3}
    )

def ask_question(question, retriever, llm, chat_history):
    history_text = ""
    for message in chat_history:
        if message["role"] == "user":
            history_text += f"User: {message['content']}\n"
        else:
            history_text += f"Assistant: {message['content']}\n"

    rewrite_question = rewrite_prompt.format(
        chat_history=history_text,
        question=question
    )

    rewritten_question = llm.invoke(rewrite_question).content

    retrieved_docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in retrieved_docs
    )

    formatted_prompt = prompt.format(
        context=context,
        rewritten_question=rewritten_question,
        chat_history=history_text
    )

    response = llm.invoke(formatted_prompt)

    return response.content