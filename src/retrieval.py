"""
Retrieval Module
ChromaDB storage and similarity search
"""

import chromadb
from chromadb.config import Settings
import pandas as pd
from typing import List, Dict, Optional
from pathlib import Path


class NewsRetriever:
    """
    Wrapper class for ChromaDB retrieval operations
    """
    
    def __init__(self, collection_name: str = "rpp_news", persist_directory: str = "./data/chromadb"):
        """
        Initialize the retriever
        
        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Directory to persist ChromaDB data
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        
        # Create persist directory
        Path(persist_directory).mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB client
        print(f"Initializing ChromaDB in: {persist_directory}")
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            print(f"Loaded existing collection: {collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            print(f"Created new collection: {collection_name}")
    
    def add_documents(self, articles: List[Dict]):
        """
        Add or upsert documents to the collection
        
        Args:
            articles: List of articles with embeddings
        """
        print(f"Adding {len(articles)} documents to collection...")
        
        documents = []
        embeddings = []
        metadatas = []
        ids = []
        
        for idx, article in enumerate(articles):
            # Document text
            text = article.get("text", f"{article.get('title', '')}\n{article.get('description', '')}")
            documents.append(text)
            
            # Embedding
            embeddings.append(article["embedding"].tolist())
            
            # Metadata
            metadata = {
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "link": article.get("link", ""),
                "published": article.get("published", "")
            }
            metadatas.append(metadata)
            
            # ID
            ids.append(f"article_{idx}")
        
        # Upsert to collection
        self.collection.upsert(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"Successfully added {len(articles)} documents")
        print(f"Total documents in collection: {self.collection.count()}")
    
    def query(self, query_text: str, n_results: int = 5, embedder=None) -> Dict:
        """
        Query the collection with similarity search
        
        Args:
            query_text: Query string
            n_results: Number of results to return
            embedder: NewsEmbedder instance for generating query embedding
            
        Returns:
            Dictionary with query results
        """
        print(f"\nQuerying: '{query_text}'")
        
        if embedder:
            # Use embedder to generate query embedding
            query_embedding = embedder.embed_text(query_text).tolist()
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
        else:
            # Use ChromaDB's default embedding (if available)
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
        
        return results
    
    def query_to_dataframe(self, query_text: str, n_results: int = 5, embedder=None) -> pd.DataFrame:
        """
        Query and return results as pandas DataFrame
        
        Args:
            query_text: Query string
            n_results: Number of results to return
            embedder: NewsEmbedder instance for generating query embedding
            
        Returns:
            DataFrame with columns: title, description, link, date_published
        """
        results = self.query(query_text, n_results, embedder)
        
        # Extract metadata from results
        data = []
        if results["metadatas"] and len(results["metadatas"]) > 0:
            for metadata in results["metadatas"][0]:
                row = {
                    "title": metadata.get("title", ""),
                    "description": metadata.get("description", ""),
                    "link": metadata.get("link", ""),
                    "date_published": metadata.get("published", "")
                }
                data.append(row)
        
        df = pd.DataFrame(data)
        return df
    
    def get_collection_stats(self) -> Dict:
        """
        Get statistics about the collection
        
        Returns:
            Dictionary with collection statistics
        """
        count = self.collection.count()
        return {
            "collection_name": self.collection_name,
            "document_count": count,
            "persist_directory": self.persist_directory
        }


if __name__ == "__main__":
    # Test the module
    from embeddings import NewsEmbedder
    
    retriever = NewsRetriever()
    print("\nCollection stats:")
    print(retriever.get_collection_stats())

