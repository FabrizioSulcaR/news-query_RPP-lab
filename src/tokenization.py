"""
Tokenization Module
Uses tiktoken to count tokens and determine if chunking is needed
"""

import tiktoken
from typing import List, Dict, Tuple


def get_tokenizer(encoding_name: str = "cl100k_base"):
    """
    Get tiktoken encoder
    
    Args:
        encoding_name: Name of the encoding to use
        
    Returns:
        Tiktoken encoder
    """
    return tiktoken.get_encoding(encoding_name)


def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    """
    Count tokens in text
    
    Args:
        text: Input text
        encoding_name: Name of the encoding to use
        
    Returns:
        Number of tokens
    """
    encoder = get_tokenizer(encoding_name)
    tokens = encoder.encode(text)
    return len(tokens)


def analyze_article_tokens(article: Dict, encoding_name: str = "cl100k_base") -> Dict:
    """
    Analyze token counts for an article
    
    Args:
        article: Article dictionary with title and description
        encoding_name: Name of the encoding to use
        
    Returns:
        Dictionary with token analysis
    """
    title = article.get("title", "")
    description = article.get("description", "")
    full_text = f"{title}\n{description}"
    
    title_tokens = count_tokens(title, encoding_name)
    description_tokens = count_tokens(description, encoding_name)
    total_tokens = count_tokens(full_text, encoding_name)
    
    return {
        "title": title,
        "title_tokens": title_tokens,
        "description_tokens": description_tokens,
        "total_tokens": total_tokens,
        "full_text": full_text
    }


def analyze_corpus_tokens(articles: List[Dict], encoding_name: str = "cl100k_base") -> Dict:
    """
    Analyze token statistics for entire corpus
    
    Args:
        articles: List of article dictionaries
        encoding_name: Name of the encoding to use
        
    Returns:
        Dictionary with corpus statistics
    """
    token_counts = []
    
    for article in articles:
        analysis = analyze_article_tokens(article, encoding_name)
        token_counts.append(analysis["total_tokens"])
    
    return {
        "num_articles": len(articles),
        "total_tokens": sum(token_counts),
        "avg_tokens": sum(token_counts) / len(token_counts) if token_counts else 0,
        "min_tokens": min(token_counts) if token_counts else 0,
        "max_tokens": max(token_counts) if token_counts else 0,
        "token_counts": token_counts
    }


def needs_chunking(text: str, max_tokens: int = 512, encoding_name: str = "cl100k_base") -> Tuple[bool, int]:
    """
    Determine if text needs chunking based on token count
    
    Args:
        text: Input text
        max_tokens: Maximum tokens allowed
        encoding_name: Name of the encoding to use
        
    Returns:
        Tuple of (needs_chunking, token_count)
    """
    token_count = count_tokens(text, encoding_name)
    return token_count > max_tokens, token_count


if __name__ == "__main__":
    # Test the module
    sample_text = "Esta es una noticia de prueba sobre economía en el Perú."
    tokens = count_tokens(sample_text)
    print(f"Sample text: {sample_text}")
    print(f"Token count: {tokens}")
    
    needs_chunk, count = needs_chunking(sample_text, max_tokens=10)
    print(f"Needs chunking (max 10): {needs_chunk}, Token count: {count}")

