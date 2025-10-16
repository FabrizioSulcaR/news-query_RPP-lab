"""
Quick Demo Script
A simple demonstration of the RPP News Retrieval System
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rss_parser import fetch_rpp_news
from tokenization import analyze_corpus_tokens
from embeddings import NewsEmbedder
from retrieval import NewsRetriever

def main():
    print("="*70)
    print("RPP NEWS RETRIEVAL SYSTEM - QUICK DEMO")
    print("="*70)
    
    # Step 1: Fetch articles
    print("\n[1/5] Fetching RSS feed from RPP...")
    articles = fetch_rpp_news(max_items=10)  # Use only 10 for quick demo
    print(f"✅ Fetched {len(articles)} articles")
    
    # Step 2: Analyze tokens
    print("\n[2/5] Analyzing token counts...")
    corpus_stats = analyze_corpus_tokens(articles)
    print(f"✅ Average tokens per article: {corpus_stats['avg_tokens']:.2f}")
    
    # Step 3: Generate embeddings
    print("\n[3/5] Generating embeddings...")
    embedder = NewsEmbedder()
    embedded_articles = embedder.embed_articles(articles)
    print(f"✅ Generated embeddings for {len(embedded_articles)} articles")
    
    # Step 4: Store in ChromaDB
    print("\n[4/5] Storing in ChromaDB...")
    retriever = NewsRetriever(
        collection_name="rpp_news_demo",
        persist_directory="./data/chromadb_demo"
    )
    retriever.add_documents(embedded_articles)
    print(f"✅ Stored {len(embedded_articles)} documents")
    
    # Step 5: Query
    print("\n[5/5] Querying the database...")
    query = "Últimas noticias de economía"
    results_df = retriever.query_to_dataframe(query, n_results=3, embedder=embedder)
    
    print(f"\n🔍 Query: '{query}'")
    print("\n📋 Top 3 Results:\n")
    
    for idx, row in results_df.iterrows():
        print(f"\n{idx+1}. {row['title']}")
        print(f"   📅 {row['date_published']}")
        print(f"   🔗 {row['link']}")
        print(f"   📝 {row['description'][:100]}...")
    
    print("\n" + "="*70)
    print("✅ DEMO COMPLETED SUCCESSFULLY!")
    print("\nFor the complete workflow, run the Jupyter notebook:")
    print("  jupyter notebook notebooks/news_retrieval_system.ipynb")
    print("="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error occurred: {e}")
        print("\nPlease ensure all dependencies are installed:")
        print("  pip install -r requirements.txt")

