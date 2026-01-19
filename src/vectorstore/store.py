"""Vector store implementations for document storage and retrieval."""

from pathlib import Path
from typing import List, Optional

from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.vectorstore.embeddings import EmbeddingSettings, get_embeddings


class VectorStoreError(Exception):
    """Raised when vector store operations fail."""
    pass


class ChromaStore:
    """ChromaDB vector store wrapper.
    
    Attributes:
        collection_name: Name of the ChromaDB collection.
        persist_directory: Directory for persistent storage.
    """
    
    def __init__(
        self,
        collection_name: str = "documents",
        persist_directory: Optional[Path] = None,
        embedding_settings: Optional[EmbeddingSettings] = None,
    ):
        """Initialize ChromaDB store.
        
        Args:
            collection_name: Name for the collection.
            persist_directory: Path for persistent storage. Uses in-memory if None.
            embedding_settings: Embedding configuration. Loads from env if None.
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self._embedding_settings = embedding_settings
        self._store: Optional[Chroma] = None
    
    @property
    def store(self) -> Chroma:
        """Lazy initialization of Chroma store."""
        if self._store is None:
            embeddings = get_embeddings(self._embedding_settings)
            
            kwargs = {
                "collection_name": self.collection_name,
                "embedding_function": embeddings,
            }
            
            if self.persist_directory:
                kwargs["persist_directory"] = str(self.persist_directory)
            
            self._store = Chroma(**kwargs)
        
        return self._store
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        """Add documents to the vector store.
        
        Args:
            documents: List of documents to add.
            
        Returns:
            List of document IDs.
            
        Raises:
            VectorStoreError: If adding documents fails.
        """
        if not documents:
            return []
        
        try:
            ids = self.store.add_documents(documents)
            return ids
        except Exception as e:
            raise VectorStoreError(f"Failed to add documents: {e}")
    
    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[dict] = None,
    ) -> List[Document]:
        """Search for similar documents.
        
        Args:
            query: Search query text.
            k: Number of results to return.
            filter: Optional metadata filter.
            
        Returns:
            List of similar documents, ordered by relevance.
        """
        return self.store.similarity_search(query, k=k, filter=filter)
    
    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        filter: Optional[dict] = None,
    ) -> List[tuple[Document, float]]:
        """Search for similar documents with relevance scores.
        
        Args:
            query: Search query text.
            k: Number of results to return.
            filter: Optional metadata filter.
            
        Returns:
            List of (document, score) tuples, ordered by relevance.
        """
        return self.store.similarity_search_with_score(query, k=k, filter=filter)
    
    def delete(self, ids: List[str]) -> None:
        """Delete documents by ID.
        
        Args:
            ids: List of document IDs to delete.
        """
        self.store.delete(ids)
    
    def count(self) -> int:
        """Get number of documents in store.
        
        Returns:
            Document count.
        """
        return len(self.store.get()["ids"])
    
    def clear(self) -> None:
        """Remove all documents from store."""
        all_ids = self.store.get()["ids"]
        if all_ids:
            self.store.delete(all_ids)
