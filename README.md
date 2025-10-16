# RPP News Retrieval and Embedding System

## 📋 Project Overview

This project implements an end-to-end **News Retrieval and Embedding System** that ingests the latest news from RPP Perú's RSS feed, generates semantic embeddings using SentenceTransformers, and enables intelligent similarity search using ChromaDB. The entire pipeline is orchestrated with LangChain for modularity and reproducibility.

### Objective

Build a retrieval system that:
- ✅ Fetches 50 latest articles from [RPP RSS Feed](https://rpp.pe/rss)
- ✅ Tokenizes articles using `tiktoken` and analyzes token counts
- ✅ Generates embeddings with `sentence-transformers/all-MiniLM-L6-v2`
- ✅ Stores documents in ChromaDB with metadata
- ✅ Performs semantic similarity search
- ✅ Orchestrates all steps with LangChain

---

## 🏗️ Project Structure

```
news-query_RPP-lab/
├── notebooks/                    # Jupyter notebooks
│   └── news_retrieval_system.ipynb  # MAIN FILE - Self-contained notebook
├── data/                         # Data storage (created at runtime)
│   ├── rss_feed.json            # Raw RSS data
│   ├── chromadb/                # ChromaDB persistence
│   └── langchain_chromadb/      # LangChain vector store
├── outputs/                      # Query results
│   ├── query_economia.csv
│   ├── query_politica.csv
│   ├── query_deportes.csv
│   └── query_langchain_economia.csv
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

**Note**: All code is self-contained in the Jupyter notebook - no external modules required!

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager
- (Optional) Virtual environment tool (venv, conda, etc.)

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd news-query_RPP-lab
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**:
   ```bash
   python -c "import feedparser, tiktoken, sentence_transformers, chromadb, langchain; print('All dependencies installed!')"
   ```

---

## 📊 Usage

### Main Notebook (Self-Contained)

The complete workflow is in a single self-contained Jupyter notebook:

```bash
jupyter notebook notebooks/news_retrieval_system.ipynb
```

Run all cells sequentially to:
1. Fetch 50 latest articles from RPP RSS feed
2. Analyze token counts using tiktoken
3. Generate embeddings with SentenceTransformers
4. Store documents in ChromaDB
5. Perform similarity search queries
6. Run LangChain end-to-end pipeline

**All functions and classes are defined directly in the notebook** - no external imports needed!

### Code Structure

The notebook contains:

- **RSS Parser Functions**: `fetch_rpp_news()`, `save_articles_to_json()`
- **Tokenization Functions**: `count_tokens()`, `analyze_article_tokens()`, `needs_chunking()`, `analyze_corpus_tokens()`
- **NewsEmbedder Class**: For generating embeddings with sentence-transformers
- **NewsRetriever Class**: For ChromaDB storage and similarity search
- **NewsRetrievalPipeline Class**: For LangChain orchestration

Simply open the notebook and run all cells sequentially!

---

## 🧮 Technical Details

### Step 0️⃣: RSS Feed Ingestion

- **Library**: `feedparser`
- **Source**: https://rpp.pe/rss
- **Output**: 50 latest articles with `title`, `description`, `link`, `published`

### Step 1️⃣: Tokenization

- **Library**: `tiktoken`
- **Encoding**: `cl100k_base` (GPT-4 tokenizer)
- **Analysis**: Token counts per article, corpus statistics, chunking decisions

### Step 2️⃣: Embeddings

- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Dimension**: 384
- **Input**: Title + Description
- **Output**: Dense vector embeddings

### Step 3️⃣: Vector Storage

- **Database**: ChromaDB
- **Similarity**: Cosine similarity
- **Features**: Metadata filtering, persistence, upsert operations

### Step 4️⃣: Query & Retrieval

- **Method**: Semantic similarity search
- **Output Format**: Pandas DataFrame with columns:
  - `title` - Article title
  - `description` - Article description
  - `link` - Article URL
  - `date_published` - Publication date

### Step 5️⃣: LangChain Orchestration

- **Components**:
  - `CharacterTextSplitter` - Text chunking
  - `HuggingFaceEmbeddings` - Embedding wrapper
  - `Chroma` - Vector store integration
- **Pipeline**: Load → Tokenize → Embed → Store → Retrieve

---

## 📈 Example Queries

The system has been tested with the following queries:

1. **"Últimas noticias de economía"** - Returns economy-related articles
2. **"Noticias sobre política"** - Returns political news
3. **"Deportes y fútbol"** - Returns sports articles

Results are displayed as pandas DataFrames and saved to CSV files in the `outputs/` directory.

---

## 📦 Dependencies

Core libraries (see `requirements.txt`):

- `feedparser>=6.0.11` - RSS feed parsing
- `tiktoken>=0.5.2` - Token counting
- `sentence-transformers>=2.2.2` - Embedding generation
- `chromadb>=0.4.22` - Vector database
- `langchain>=0.1.0` - LLM orchestration
- `langchain-community>=0.0.10` - Community integrations
- `pandas>=2.0.3` - Data manipulation
- `jupyter>=1.0.0` - Interactive notebooks

---

## 🎯 Deliverables Checklist

### Data & Reproducibility — 4 pts

- ✅ Organized repository structure (`/src`, `/data`, `/notebooks`, `/outputs`)
- ✅ Functional Jupyter notebook provided
- ✅ All file paths are relative, no absolute directories
- ✅ Complete and functional `requirements.txt` file included
- ✅ Code runs end-to-end without manual intervention

### Task 1: Retrieval System — 6 pts

- ✅ Correct RSS parsing from RPP feed (https://rpp.pe/rss)
- ✅ Proper tokenization and token count verification using tiktoken
- ✅ Generation of embeddings with SentenceTransformers/all-MiniLM-L6-v2
- ✅ Creation and management of a ChromaDB collection (store + upsert + retrieval)
- ✅ LangChain orchestration connecting all steps (load → tokenize → embed → store → query)
- ✅ Clear output table displaying: `title | description | link | date_published`

### No Penalties

- ✅ Complete and informative README.md
- ✅ Complete requirements.txt with correct dependencies
- ✅ Fully reproducible results with relative paths
- ✅ Clear result documentation and outputs

---

## 🔬 Expected Outputs

### Console Output

The notebook produces detailed console output for each step:

```
✅ All imports successful!
📊 Total articles fetched: 50
🔤 Token Analysis for Sample Article:
   Title tokens: 12
   Description tokens: 45
   Total tokens: 57
✅ Embeddings generated for 50 articles
📊 Collection Statistics:
   Collection name: rpp_news
   Document count: 50
🔍 Query: 'Últimas noticias de economía'
📋 Top 5 Results: [DataFrame displayed]
```

### CSV Outputs

Query results are saved to `outputs/` directory:

- `query_economia.csv` - Economy-related articles
- `query_politica.csv` - Political news articles
- `query_deportes.csv` - Sports articles
- `query_langchain_economia.csv` - LangChain pipeline results

Each CSV contains columns: `title`, `description`, `link`, `date_published`

---

## 🔧 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. **RSS Feed Access**: If the RSS feed is unreachable, check your internet connection or verify the URL is still active.

3. **ChromaDB Permission Issues**: Ensure the `data/` directory has write permissions.

4. **Memory Issues**: The sentence-transformers model requires ~100MB RAM. Ensure sufficient resources.

---

## 📝 Notes

- **Self-Contained**: All code is embedded in the notebook - no external modules needed
- **Relative Paths**: All file paths are relative for cross-environment reproducibility
- **Persistent Storage**: ChromaDB collections are persisted for faster subsequent runs
- **Deterministic**: Results are consistent given the same RSS feed state
- **Google Colab Compatible**: Add `!pip install -r requirements.txt` at the start

---

## 📄 License

This project is for educational purposes as part of the RPP Lab assignment.

---

## 👥 Authors

**FabrizioSulcaR** and **Verachamochumbi**  
CyberProyectos Lab  
---

## 📞 Support

For issues or questions, please refer to:
1. The Jupyter notebook documentation
2. Individual module docstrings in `src/`
3. This README file

---

**Last Updated**: October 16, 2025

