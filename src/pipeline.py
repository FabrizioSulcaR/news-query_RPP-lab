"""
LangChain Pipeline Module
End-to-end orchestration of the news retrieval system
"""

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from typing import List, Dict
import pandas as pd


class NewsRetrievalPipeline:
    """
    LangChain-based pipeline for news retrieval
    """
    
    def __init__(self, 
                 model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                 persist_directory: str = "./data/langchain_chromadb"):
        """
        Initialize the pipeline
        
        Args:
            model_name: Name of the embedding model
            persist_directory: Directory to persist vector store
        """
        print("Initializing LangChain NewsRetrievalPipeline...")
        
        self.model_name = model_name
        self.persist_directory = persist_directory
        
        # Initialize embeddings
        print(f"Loading embeddings model: {model_name}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Text splitter (for chunking if needed)
        self.text_splitter = CharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separator="\n"
        )
        
        self.vectorstore = None
        print("Pipeline initialized successfully")
    
    def load_articles_as_documents(self, articles: List[Dict]) -> List[Document]:
        """
        Convert articles to LangChain Document objects
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            List of LangChain Document objects
        """
        print(f"Converting {len(articles)} articles to LangChain Documents...")
        
        documents = []
        for article in articles:
            # Combine title and description
            page_content = f"{article.get('title', '')}\n{article.get('description', '')}"
            
            # Metadata
            metadata = {
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "link": article.get("link", ""),
                "published": article.get("published", "")
            }
            
            doc = Document(page_content=page_content, metadata=metadata)
            documents.append(doc)
        
        print(f"Created {len(documents)} documents")
        return documents
    
    def create_vectorstore(self, documents: List[Document]) -> Chroma:
        """
        Create or update Chroma vector store with documents
        
        Args:
            documents: List of LangChain Document objects
            
        Returns:
            Chroma vector store
        """
        print(f"Creating vector store with {len(documents)} documents...")
        
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        print(f"Vector store created and persisted to: {self.persist_directory}")
        return self.vectorstore
    
    def load_vectorstore(self) -> Chroma:
        """
        Load existing vector store
        
        Returns:
            Chroma vector store
        """
        print(f"Loading vector store from: {self.persist_directory}")
        
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
        
        print("Vector store loaded successfully")
        return self.vectorstore
    
    def query(self, query_text: str, k: int = 5) -> List[Document]:
        """
        Query the vector store
        
        Args:
            query_text: Query string
            k: Number of results to return
            
        Returns:
            List of relevant Document objects
        """
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Call create_vectorstore or load_vectorstore first.")
        
        print(f"\nQuerying: '{query_text}'")
        results = self.vectorstore.similarity_search(query_text, k=k)
        print(f"Found {len(results)} results")
        
        return results
    
    def query_to_dataframe(self, query_text: str, k: int = 5) -> pd.DataFrame:
        """
        Query and return results as pandas DataFrame
        
        Args:
            query_text: Query string
            k: Number of results to return
            
        Returns:
            DataFrame with columns: title, description, link, date_published
        """
        results = self.query(query_text, k)
        
        data = []
        for doc in results:
            row = {
                "title": doc.metadata.get("title", ""),
                "description": doc.metadata.get("description", ""),
                "link": doc.metadata.get("link", ""),
                "date_published": doc.metadata.get("published", "")
            }
            data.append(row)
        
        df = pd.DataFrame(data)
        return df
    
    def run_pipeline(self, articles: List[Dict], query_text: str, k: int = 5) -> pd.DataFrame:
        """
        Run the complete pipeline: load → embed → store → query
        
        Args:
            articles: List of article dictionaries
            query_text: Query string
            k: Number of results to return
            
        Returns:
            DataFrame with query results
        """
        print("\n" + "="*60)
        print("RUNNING COMPLETE LANGCHAIN PIPELINE")
        print("="*60)
        
        # Step 1: Load articles as documents
        print("\n[Step 1/4] Loading articles as documents...")
        documents = self.load_articles_as_documents(articles)
        
        # Step 2: Create vector store
        print("\n[Step 2/4] Creating vector store with embeddings...")
        self.create_vectorstore(documents)
        
        # Step 3: Query
        print("\n[Step 3/4] Querying vector store...")
        
        # Step 4: Return results as DataFrame
        print("\n[Step 4/4] Formatting results...")
        df = self.query_to_dataframe(query_text, k)
        
        print("\n" + "="*60)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("="*60)
        
        return df


if __name__ == "__main__":
    # Test the module
    pipeline = NewsRetrievalPipeline()
    
    sample_articles = [
        {
            "title": "Economía peruana creció 3%",
            "description": "El sector económico mostró un crecimiento sostenido",
            "link": "https://example.com/1",
            "published": "2025-10-16"
        },
        {
            "title": "Noticias de política",
            "description": "El congreso aprobó nueva ley",
            "link": "https://example.com/2",
            "published": "2025-10-16"
        }
    ]
    
    print("\nTesting pipeline with sample data...")

