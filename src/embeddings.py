"""
Embeddings Module
Generates embeddings using SentenceTransformers
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict


class NewsEmbedder:
    """
    Wrapper class for generating news embeddings
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the embedder
        
        Args:
            model_name: Name of the SentenceTransformer model
        """
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        print(f"Model loaded successfully. Embedding dimension: {self.model.get_sentence_embedding_dimension()}")
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector as numpy array
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    def embed_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Generate embeddings for multiple articles
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            List of articles with embeddings added
        """
        print(f"Generating embeddings for {len(articles)} articles...")
        
        # Prepare texts (title + description)
        texts = []
        for article in articles:
            title = article.get("title", "")
            description = article.get("description", "")
            text = f"{title}\n{description}"
            texts.append(text)
        
        # Generate embeddings in batch
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        
        # Add embeddings to articles
        embedded_articles = []
        for article, embedding in zip(articles, embeddings):
            embedded_article = article.copy()
            embedded_article["embedding"] = embedding
            embedded_article["text"] = f"{article.get('title', '')}\n{article.get('description', '')}"
            embedded_articles.append(embedded_article)
        
        print(f"Embeddings generated. Shape: {embeddings.shape}")
        return embedded_articles
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings
        
        Returns:
            Embedding dimension
        """
        return self.model.get_sentence_embedding_dimension()


if __name__ == "__main__":
    # Test the module
    embedder = NewsEmbedder()
    
    sample_article = {
        "title": "Noticias de economía",
        "description": "El Banco Central aumentó la tasa de interés",
        "link": "https://example.com",
        "published": "2025-10-16"
    }
    
    embedded = embedder.embed_articles([sample_article])
    print(f"\nSample embedding shape: {embedded[0]['embedding'].shape}")
    print(f"First 10 values: {embedded[0]['embedding'][:10]}")

