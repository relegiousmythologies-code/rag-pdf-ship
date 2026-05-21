# PDF RAG Pipeline - Complete Implementation

This directory contains a **production-ready PDF Retrieval-Augmented Generation (RAG) pipeline** for uploading PDFs, extracting text via OCR, storing embeddings, and querying with an LLM.

## 🎯 Quick Start (3 Commands)

```bash
# 1. Start all services
docker-compose up -d

# 2. Download LLM model
docker exec pdf_pipeline_ollama ollama pull mistral

# 3. Upload and query
python cli.py --upload your_document.pdf
python cli.py --query "What is this document about?"
```

## 📋 Features

✅ **PDF Upload & Processing**
- Multi-file upload support
- Automatic OCR text extraction (fallback for scanned PDFs)
- Intelligent chunking with overlap
- Progress tracking

✅ **Vector Storage**
- GPU-ready embeddings (HuggingFace)
- Chroma vector database
- Persistent storage
- Easy retrieval

✅ **LLM Query Interface**
- Local Ollama models (free)
- Fast inference
- Source citations
- Multi-turn conversations

✅ **Easy-to-Use CLI**
- Single-command upload
- Interactive query mode
- Status monitoring
- API integration ready

## 📁 Files

| File | Purpose |
|------|---------|
| `pdf_processor.py` | PDF extraction & OCR service |
| `query_engine.py` | LLM generation & retrieval service |
| `cli.py` | Command-line interface |
| `docker-compose.yml` | Service orchestration |
| `Dockerfile.processor` | Processor container |
| `Dockerfile.query` | Query engine container |
| `requirements.txt` | Python dependencies |
| `SETUP.md` | Detailed setup guide |

## 🚀 Usage

### Upload PDFs
```bash
python cli.py --upload doc1.pdf doc2.pdf doc3.pdf
```

### Query
```bash
# Single query
python cli.py --query "What is the main topic?"

# Interactive mode
python cli.py --interactive

# With custom result count
python cli.py --query "Question?" --num-results 5
```

### Status & Management
```bash
# Check system status
python cli.py --status

# Clear database (API)
curl -X POST http://localhost:8000/clear
```

## 🏗️ Architecture

```
Your PDFs
   ↓
[PDF Processor Service]
   ├─ Extract text (OCR)
   ├─ Chunk text (1000 chars)
   └─ Create embeddings
   ↓
[Chroma Vector DB]
   ├─ Store embeddings
   └─ Metadata tracking
   ↓
[Query Engine Service]
   ├─ Retrieve relevant chunks
   ├─ Pass to Ollama LLM
   └─ Generate answer
   ↓
You get: Answer + Sources
```

## ⚙️ API Endpoints

### Processor Service (Port 8000)
- `POST /upload` - Upload PDFs
- `GET /status` - Service status
- `GET /health` - Health check
- `POST /clear` - Clear database

### Query Engine (Port 8001)
- `POST /query` - Query documents
- `GET /status` - Service status
- `GET /health` - Health check
- `GET /models` - Available LLM models

## 🔧 Configuration

Edit configuration in service files:

**PDF Processing** (pdf_processor.py):
```python
CHUNK_SIZE = 1000           # Character size per chunk
CHUNK_OVERLAP = 200         # Overlap between chunks
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
```

**LLM Generation** (query_engine.py):
```python
LLM_MODEL = "mistral"       # Change to neural-chat, orca-mini, etc.
NUM_RESULTS = 3             # Number of context chunks
```

## 📦 Available LLM Models

- **mistral** - Good balance (fastest)
- **neural-chat** - Lightweight & quick
- **orca-mini** - Very fast
- **llama2** - More powerful
- **dolphin-mixtral** - Advanced

Download with: `docker exec pdf_pipeline_ollama ollama pull <model>`

## 📊 Requirements

- **RAM**: 8GB+ (more for larger models)
- **Disk**: 20GB+ (for LLM models + data)
- **Docker**: Latest version
- **Internet**: For initial model download

## 🆘 Troubleshooting

See [SETUP.md](SETUP.md) for detailed troubleshooting guide.

### Quick Checks
```bash
# Check service logs
docker-compose logs -f

# Test processor
curl http://localhost:8000/health

# Test query engine
curl http://localhost:8001/health

# Verify Ollama
docker exec pdf_pipeline_ollama ollama list
```

## 📚 Example Queries

```bash
# Ask about content
python cli.py --query "What is the main topic?"

# Get summaries
python cli.py --query "Summarize the key points"

# Find specific info
python cli.py --query "What does section 3 discuss?"

# Comparative questions
python cli.py --query "Compare the two documents"
```

## 🎯 Next Steps

1. Read [SETUP.md](SETUP.md) for detailed setup
2. Run `python quickstart.py` for automated setup
3. Upload your first PDF
4. Start querying!

---

**Built with:**
- LangChain - Orchestration
- Chroma - Vector Database
- HuggingFace - Embeddings
- Ollama - Local LLM Runtime
- FastAPI - APIs

**License**: Apache 2.0
