"""Embedding providers for vector generation."""

from enum import Enum
from typing import List

from langchain_openai import OpenAIEmbeddings
from pydantic_settings import BaseSettings, SettingsConfigDict


class EmbeddingProvider(str, Enum):
    """Available embedding providers."""
    OPENAI = "openai"


class EmbeddingSettings(BaseSettings):
    """Settings for embedding configuration."""
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    openai_api_key: str = ""
    embedding_provider: EmbeddingProvider = EmbeddingProvider.OPENAI
    embedding_model: str = "text-embedding-ada-002"


def get_embeddings(settings: EmbeddingSettings | None = None) -> OpenAIEmbeddings:
    """Get configured embedding model.
    
    Args:
        settings: Embedding settings. Loads from environment if None.
        
    Returns:
        Configured embedding model instance.
        
    Raises:
        ValueError: If API key not configured.
    """
    if settings is None:
        settings = EmbeddingSettings()
    
    if settings.embedding_provider == EmbeddingProvider.OPENAI:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")
        
        return OpenAIEmbeddings(
            api_key=settings.openai_api_key,
            model=settings.embedding_model,
        )
    
    raise ValueError(f"Unknown embedding provider: {settings.embedding_provider}")


def embed_texts(texts: List[str], settings: EmbeddingSettings | None = None) -> List[List[float]]:
    """Generate embeddings for a list of texts.
    
    Args:
        texts: List of text strings to embed.
        settings: Embedding settings. Loads from environment if None.
        
    Returns:
        List of embedding vectors.
    """
    embeddings = get_embeddings(settings)
    return embeddings.embed_documents(texts)


def embed_query(query: str, settings: EmbeddingSettings | None = None) -> List[float]:
    """Generate embedding for a single query.
    
    Args:
        query: Query text to embed.
        settings: Embedding settings. Loads from environment if None.
        
    Returns:
        Embedding vector for the query.
    """
    embeddings = get_embeddings(settings)
    return embeddings.embed_query(query)
