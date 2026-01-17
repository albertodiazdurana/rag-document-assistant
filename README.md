# RAG Document Assistant

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-orange.svg)](https://langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Production-ready RAG system with multi-provider LLM support (OpenAI, Claude, Ollama), vector database integration, FastAPI backend, and MLflow evaluation. Features German language support and Streamlit UI.

## What This Does

Imagine you have hundreds of documents; manuals, reports, contracts. Instead of reading through all of them to find an answer, you simply ask a question in plain language: *"What are the warranty terms for product X?"* or *"Summarize the key findings from last quarter."*

This application reads your documents, understands their content, and answers your questions accurately; citing exactly where it found the information. It works in both English and German, and you can choose which AI assistant (ChatGPT, Claude, or a private local model) answers your questions.

## Features

- **Multi-Provider LLM Support**: OpenAI GPT-4o, Anthropic Claude, Ollama (local models)
- **Vector Database Integration**: ChromaDB (local), Pinecone (cloud)
- **Document Processing**: PDF, Markdown, TXT with configurable chunking
- **FastAPI Backend**: REST API with async document processing
- **MLflow Evaluation**: Experiment tracking with custom RAG metrics
- **German Language Support**: Multilingual embeddings and prompts
- **Streamlit UI**: Interactive document upload and chat interface
- **Hybrid Search**: Semantic + keyword (BM25) retrieval

## Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key (or Anthropic/Ollama for alternative providers)

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/rag-document-assistant.git
cd rag-document-assistant

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"
```

### Environment Setup

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys
# Required: OPENAI_API_KEY
# Optional: ANTHROPIC_API_KEY, PINECONE_API_KEY
```

### Run the Application

```bash
# Start FastAPI backend
uvicorn src.api.main:app --reload

# In another terminal, start Streamlit UI
streamlit run app/streamlit_app.py
```

## Project Structure

```
rag-document-assistant/
├── src/
│   ├── ingestion/          # Document loaders and chunking
│   ├── vectorstore/        # Embeddings and vector database
│   ├── retrieval/          # RAG chain and reranking
│   ├── llm/                # LLM providers and prompts
│   ├── api/                # FastAPI backend
│   └── evaluation/         # MLflow metrics
├── app/
│   └── streamlit_app.py    # Streamlit interface
├── tests/                  # Unit and integration tests
├── data/
│   └── sample_docs/        # Example documents
└── docs/                   # Architecture documentation
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/ingest` | POST | Upload and index documents |
| `/query` | POST | Query the RAG system |
| `/models` | GET | List available LLM providers |

## Configuration

### LLM Providers

```python
# OpenAI (default)
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...

# Anthropic Claude
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Ollama (local, no API key needed)
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
```

### Vector Database

```python
# ChromaDB (default, local)
VECTOR_DB=chroma

# Pinecone (cloud)
VECTOR_DB=pinecone
PINECONE_API_KEY=...
PINECONE_INDEX=rag-documents
```

## Hardware Requirements

**No GPU required.** This project uses API-based LLMs and embeddings:

| Component | Compute Location | Local Requirements |
|-----------|------------------|-------------------|
| LLM Inference | OpenAI/Claude API | Internet connection |
| Embeddings | OpenAI API | Internet connection |
| Vector Search | Local (ChromaDB) | ~4GB RAM |
| Ollama (optional) | Local CPU/GPU | 8GB+ RAM |

Works on Windows, macOS, and Linux.

## Development

```bash
# Run tests
pytest tests/ -v --cov=src

# Format code
black src/ tests/
ruff check src/ tests/

# Type checking
mypy src/
```

## Evaluation with MLflow

```bash
# Start MLflow UI
mlflow ui

# Run evaluation pipeline
python -m src.evaluation.run_eval
```

Tracked metrics:
- **Faithfulness**: Answer grounded in retrieved context
- **Relevance**: Retrieved chunks match query intent
- **Latency**: End-to-end response time

## Tech Stack

| Category | Technologies |
|----------|--------------|
| **LLM Orchestration** | LangChain, LangGraph |
| **LLM Providers** | OpenAI, Anthropic, Ollama |
| **Vector Database** | ChromaDB, Pinecone |
| **Embeddings** | OpenAI ada-002, HuggingFace multilingual-e5 |
| **Backend** | FastAPI, Pydantic, uvicorn |
| **Evaluation** | MLflow |
| **UI** | Streamlit |
| **Testing** | pytest, pytest-cov |

## Roadmap

- [x] Project setup
- [ ] Document ingestion pipeline
- [ ] Vector database integration
- [ ] RAG chain with LLM providers
- [ ] FastAPI backend
- [ ] MLflow evaluation
- [ ] Streamlit UI
- [ ] German language support
- [ ] Hybrid search (BM25 + semantic)
- [ ] Docker deployment

## License

MIT License

## Author

Alberto Díaz-Durana
