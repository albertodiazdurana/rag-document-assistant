# RAG Document Assistant

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-orange.svg)](https://langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Production-ready RAG system with multi-provider LLM support (OpenAI, Anthropic, Ollama), ChromaDB vector database, FastAPI backend, and MLflow evaluation.

## What This Does

Imagine you have hundreds of documents; manuals, reports, contracts. Instead of reading through all of them to find an answer, you simply ask a question in plain language: *"What are the warranty terms for product X?"* or *"Summarize the key findings from last quarter."*

This application reads your documents, understands their content, and answers your questions accurately; citing exactly where it found the information. You can choose which AI provider (OpenAI, Anthropic, or a local Ollama model) answers your questions.

## Features

### Implemented (Sprint 1)

- **Multi-Provider LLM Support**: OpenAI, Anthropic, Ollama (local models)
- **Vector Database**: ChromaDB with OpenAI embeddings
- **Document Processing**: PDF, Markdown, TXT with configurable chunking
- **RAG Chain**: Retrieval-augmented generation with conversation memory
- **FastAPI Backend**: REST API with async document processing
- **MLflow Evaluation**: Experiment tracking with faithfulness/relevance metrics

### Planned (Sprint 2)

- **Streamlit UI**: Interactive document upload and chat interface
- **German Language Support**: Multilingual embeddings and prompts
- **Pinecone Integration**: Cloud vector database option
- **Hybrid Search**: Semantic + keyword (BM25) retrieval
- **Docker Deployment**: Containerized production setup

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
# Required: OPENAI_API_KEY (for embeddings)
# Optional: ANTHROPIC_API_KEY (for Claude LLM)
```

### Run the Application

```bash
# Start FastAPI backend
uvicorn src.api.main:app --reload

# API docs available at http://localhost:8000/docs
```

## Project Structure

```
rag-document-assistant/
├── src/
│   ├── ingestion/          # Document loaders and chunking
│   ├── vectorstore/        # Embeddings and vector database
│   ├── retrieval/          # RAG chain with memory
│   ├── llm/                # LLM providers and prompts
│   ├── api/                # FastAPI backend
│   └── evaluation/         # MLflow metrics
├── tests/                  # Unit tests (84 tests)
├── data/
│   ├── sample_docs/        # Example documents
│   └── eval/               # Evaluation test dataset
└── docs/
    ├── checkpoints/        # Sprint progress
    └── decisions/          # Architecture decisions
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/v1/ingest` | POST | Upload and index documents |
| `/api/v1/query` | POST | Query the RAG system |
| `/api/v1/models` | GET | List available LLM providers |
| `/api/v1/documents/count` | GET | Get indexed document count |
| `/api/v1/documents` | DELETE | Clear all documents |

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
CHROMA_PERSIST_DIR=./chroma_db
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
python -m src.evaluation.runner
```

Tracked metrics:
- **Faithfulness**: Answer grounded in retrieved context
- **Relevance**: Retrieved chunks match query intent
- **Latency**: End-to-end response time

## Tech Stack

| Category | Technologies |
|----------|--------------|
| **LLM Orchestration** | LangChain |
| **LLM Providers** | OpenAI, Anthropic, Ollama |
| **Vector Database** | ChromaDB |
| **Embeddings** | OpenAI text-embedding-ada-002 |
| **Backend** | FastAPI, Pydantic, uvicorn |
| **Evaluation** | MLflow |
| **Testing** | pytest, pytest-cov (84 tests, 73% coverage) |

## Known Limitations

This MVP has the following limitations documented in [EXP-001](docs/experiments/EXP-001_multi-source-detection.md):

| Limitation | Workaround |
|------------|------------|
| Simple queries may only cite one source | Ask "What do all documents say about X?" |
| No automatic version/date awareness | Name files with dates (e.g., `policy_2024.md`) |
| Documents persist until manually cleared | Use "Clear All Documents" button in UI |
| Relies on LLM reasoning for conflict detection | Ask explicitly about differences between sources |

**Getting Better Results:**
- Ask "Compare sources on X" to see differences
- Ask "Are there different answers for X?" for comprehensive coverage
- Use specific questions for precise answers

## Roadmap

### Sprint 1 (Complete)
- [x] Project setup
- [x] Document ingestion pipeline (PDF, MD, TXT)
- [x] Vector database integration (ChromaDB)
- [x] RAG chain with multi-provider LLM support
- [x] FastAPI backend with REST API
- [x] MLflow evaluation framework

### Sprint 2 (In Progress)
- [x] Streamlit UI
- [ ] German language support
- [ ] Pinecone cloud vector database
- [ ] Hybrid search (BM25 + semantic)
- [ ] Docker deployment

## License

MIT License

## Author

Alberto Díaz-Durana
