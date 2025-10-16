"""
Quick validation script to test the setup
Run this to verify all modules can be imported correctly
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from rss_parser import fetch_rpp_news
        print("✅ rss_parser module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import rss_parser: {e}")
        return False
    
    try:
        from tokenization import count_tokens, analyze_article_tokens
        print("✅ tokenization module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import tokenization: {e}")
        return False
    
    try:
        from embeddings import NewsEmbedder
        print("✅ embeddings module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import embeddings: {e}")
        return False
    
    try:
        from retrieval import NewsRetriever
        print("✅ retrieval module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import retrieval: {e}")
        return False
    
    try:
        from pipeline import NewsRetrievalPipeline
        print("✅ pipeline module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import pipeline: {e}")
        return False
    
    return True

def test_dependencies():
    """Test that all required dependencies are installed"""
    print("\nTesting dependencies...")
    
    dependencies = [
        'feedparser',
        'tiktoken',
        'sentence_transformers',
        'chromadb',
        'langchain',
        'langchain_community',
        'pandas',
        'numpy'
    ]
    
    all_ok = True
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} installed")
        except ImportError:
            print(f"❌ {dep} NOT installed")
            all_ok = False
    
    return all_ok

def main():
    print("="*60)
    print("RPP News Retrieval System - Setup Validation")
    print("="*60)
    
    imports_ok = test_imports()
    deps_ok = test_dependencies()
    
    print("\n" + "="*60)
    if imports_ok and deps_ok:
        print("✅ All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Open notebooks/news_retrieval_system.ipynb")
        print("2. Run all cells to execute the complete pipeline")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nTo install dependencies, run:")
        print("  pip install -r requirements.txt")
    print("="*60)

if __name__ == "__main__":
    main()

