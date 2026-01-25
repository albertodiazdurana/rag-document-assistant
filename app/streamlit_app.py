"""Streamlit UI for RAG Document Assistant."""

import streamlit as st
import requests
from typing import Dict, List, Any, Optional
import time

# Configuration
API_BASE_URL = "http://localhost:8000"
API_TIMEOUT = 30  # seconds

# Page config
st.set_page_config(
    page_title="RAG Document Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# HTTP Client Functions
def check_backend_health() -> bool:
    """Check if FastAPI backend is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def get_available_models() -> List[str]:
    """Get list of available LLM providers."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/models", timeout=5)
        response.raise_for_status()
        providers = response.json()["providers"]
        return [p["provider"] for p in providers]
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch models: {e}")
        return ["openai"]  # Default fallback


def get_document_count() -> int:
    """Get count of indexed documents."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/documents/count", timeout=5)
        response.raise_for_status()
        return response.json()["count"]
    except requests.exceptions.RequestException:
        return 0


def ingest_document(file_content: bytes, filename: str) -> Dict[str, Any]:
    """Upload and index a document."""
    files = {"files": (filename, file_content)}
    response = requests.post(
        f"{API_BASE_URL}/api/v1/ingest",
        files=files,
        timeout=API_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def query_rag(question: str, provider: str = "openai") -> Dict[str, Any]:
    """Query the RAG system."""
    payload = {
        "question": question,
        "provider": provider
    }
    response = requests.post(
        f"{API_BASE_URL}/api/v1/query",
        json=payload,
        timeout=API_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def clear_all_documents() -> Dict[str, Any]:
    """Clear all indexed documents."""
    response = requests.delete(
        f"{API_BASE_URL}/api/v1/documents",
        timeout=API_TIMEOUT
    )
    response.raise_for_status()
    return response.json()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "provider" not in st.session_state:
    st.session_state.provider = "openai"

if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()


# Sidebar
with st.sidebar:
    st.title("📚 RAG Assistant")
    
    # Backend health check
    if check_backend_health():
        st.success("✅ Backend connected")
    else:
        st.error("❌ Backend offline. Start FastAPI server.")
        st.code("uvicorn src.api.main:app --reload", language="bash")
        st.stop()
    
    st.divider()
    
    # LLM Provider Selection
    st.subheader("⚙️ Settings")
    available_models = get_available_models()
    provider = st.selectbox(
        "LLM Provider",
        options=available_models,
        index=available_models.index(st.session_state.provider) if st.session_state.provider in available_models else 0,
        help="Choose which AI model answers your questions"
    )
    st.session_state.provider = provider
    
    st.divider()
    
    # Document Upload
    st.subheader("📤 Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose files",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True,
        help="Supported formats: PDF, TXT, Markdown"
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Create unique file identifier
            file_id = f"{uploaded_file.name}_{uploaded_file.size}"

            # Only process if not already processed
            if file_id not in st.session_state.processed_files:
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    try:
                        file_content = uploaded_file.read()
                        result = ingest_document(file_content, uploaded_file.name)
                        st.success(f"✅ {uploaded_file.name}: {result['message']}")
                        st.caption(f"Added {result['chunks_created']} chunks")
                        st.session_state.processed_files.add(file_id)
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ {uploaded_file.name}: Upload failed - {e}")
            else:
                st.info(f"✓ {uploaded_file.name} already uploaded")

        # Rerun after processing all files
        if any(f"{f.name}_{f.size}" not in st.session_state.processed_files for f in uploaded_files):
            time.sleep(1)
            st.rerun()
    
    st.divider()
    
    # Document Management
    st.subheader("📊 Document Stats")
    doc_count = get_document_count()
    st.metric("Indexed Documents", doc_count)
    
    if doc_count > 0:
        if st.button("🗑️ Clear All Documents", type="secondary", use_container_width=True):
            try:
                with st.spinner("Clearing documents..."):
                    result = clear_all_documents()
                    st.success(f"✅ {result['message']}")
                    st.session_state.messages = []  # Clear chat history
                    st.session_state.processed_files = set()  # Clear processed files
                    time.sleep(1)
                    st.rerun()
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Failed to clear: {e}")
    
    st.divider()

    # Help & Limitations
    with st.expander("ℹ️ Tips & Limitations"):
        st.markdown("""
**Getting Better Results:**
- Ask "What do all documents say about X?" for comprehensive answers
- Ask "Compare sources on X" to see differences
- Use specific questions for precise answers

**Known Limitations:**
- Simple queries may only cite one source even if multiple exist
- No automatic version/date awareness between documents
- Documents persist until manually cleared

**Memory Management:**
- Documents remain indexed until you click "Clear All Documents"
- Chat history is stored in your browser session
- Refresh the page to clear chat history only
        """)

    st.divider()

    # Footer
    st.caption("Built with FastAPI + LangChain + Streamlit")


# Main Chat Area
st.title("💬 Ask Questions About Your Documents")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display sources if available
        if message["role"] == "assistant" and "sources" in message:
            with st.expander("📄 View Sources", expanded=False):
                for idx, source in enumerate(message["sources"], 1):
                    st.markdown(f"**Source {idx}:** {source['metadata'].get('source', 'Unknown')}")
                    st.caption(source["content"][:300] + "..." if len(source["content"]) > 300 else source["content"])
                    if idx < len(message["sources"]):
                        st.divider()

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Check if documents are indexed
    if get_document_count() == 0:
        st.warning("⚠️ Please upload documents first before asking questions.")
    else:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = query_rag(prompt, st.session_state.provider)
                    answer = response["answer"]
                    sources = response.get("sources", [])
                    
                    # Display answer
                    st.markdown(answer)
                    
                    # Display sources
                    if sources:
                        with st.expander("📄 View Sources", expanded=False):
                            for idx, source in enumerate(sources, 1):
                                st.markdown(f"**Source {idx}:** {source['metadata'].get('source', 'Unknown')}")
                                st.caption(source["content"][:300] + "..." if len(source["content"]) > 300 else source["content"])
                                if idx < len(sources):
                                    st.divider()
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
                    
                except requests.exceptions.RequestException as e:
                    error_msg = f"❌ Query failed: {e}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })

# Welcome message when no chat history
if len(st.session_state.messages) == 0:
    st.info("👋 Welcome! Upload documents using the sidebar, then ask questions about them.")
