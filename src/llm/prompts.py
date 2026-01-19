"""Prompt templates for RAG system."""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# System prompt for RAG with source attribution
RAG_SYSTEM_PROMPT = """You are a helpful assistant that answers questions based on the provided context.

Instructions:
1. Answer the question using ONLY the information from the context below.
2. If the context doesn't contain enough information to answer, say "I don't have enough information to answer this question."
3. Always cite your sources by referencing the document names when possible.
4. Be concise and direct in your answers.

Context:
{context}"""

# Basic RAG prompt (no chat history)
RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", RAG_SYSTEM_PROMPT),
    ("human", "{question}"),
])

# RAG prompt with conversation history
RAG_CHAT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", RAG_SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])

# Standalone question prompt (for reformulating with history)
CONDENSE_QUESTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Given the following conversation and a follow-up question, rephrase the follow-up question to be a standalone question that captures all necessary context.

Chat History:
{chat_history}

Follow-up Question: {question}

Standalone Question:"""),
])


def format_documents(documents: list) -> str:
    """Format documents for inclusion in prompt context.
    
    Args:
        documents: List of Document objects.
        
    Returns:
        Formatted string with document contents and sources.
    """
    formatted = []
    for i, doc in enumerate(documents, 1):
        source = doc.metadata.get("source", "Unknown")
        content = doc.page_content.strip()
        formatted.append(f"[Document {i}] (Source: {source})\n{content}")
    
    return "\n\n---\n\n".join(formatted)
