# PDF RAG Pipeline - Setup Guide

## 📋 Prerequisites

- Docker & Docker Compose (latest version)
- 8GB+ RAM
- 20GB+ disk space (for LLM models)
- Internet connection (for initial model download)

## 🚀 Quick Setup (Recommended)

The easiest way to get started:

```bash
cd pdf_pipeline
python quickstart.py
```

This automatically:
1. ✅ Checks Docker
2. ✅ Creates directories
3. ✅ Builds and starts all services
4. ✅ Downloads the LLM model
5. ✅ Shows you next steps

## 🛠️ Manual Setup

### Step 1: Build and Start Services

```bash
cd pdf_pipeline
docker-compose up -d
```

Wait for all services to be healthy:
```bash
docker-compose ps
```

### Step 2: Download LLM Model

```bash
# Download Mistral (default, ~4GB)
docker exec pdf_pipeline_ollama ollama pull mistral

# Or choose another model:
# docker exec pdf_pipeline_ollama ollama pull neural-chat
# docker exec pdf_pipeline_ollama ollama pull orca-mini
# docker exec pdf_pipeline_ollama ollama pull llama2
```

### Step 3: Verify Services

Check that all services are running:

```bash
# Processor health
curl http://localhost:8000/health

# Query engine health
curl http://localhost:8001/health

# Ollama models
docker exec pdf_pipeline_ollama ollama list
```

## 📤 Upload PDFs

### Using CLI (Recommended)

```bash
# Single file
python cli.py --upload document.pdf

# Multiple files
python cli.py --upload doc1.pdf doc2.pdf doc3.pdf

# Check upload status
python cli.py --status
```

### Using API

```bash
curl -X POST http://localhost:8000/upload \
  -F "files=@document.pdf"
```

## ❓ Query Documents

### Using CLI

```bash
# Single query
python cli.py --query "What is this document about?"

# Interactive mode (continuous questions)
python cli.py --interactive

# With custom result count
python cli.py --query "Question?" --num-results 5
```

### Using API

```bash
curl -X POST http://localhost:8001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Your question here", "num_results": 3}'
```

## 🔧 Configuration

### Change LLM Model

Edit `query_engine.py`:
```python
LLM_MODEL = "mistral"  # Change to your preferred model
```

Then restart:
```bash
docker-compose restart query-engine
```

### Adjust Chunk Size

Edit `pdf_processor.py`:
```python
CHUNK_SIZE = 1000        # Increase for larger chunks
CHUNK_OVERLAP = 200      # Overlap between chunks
```

### Change Embedding Model

Edit both services:
```python
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Default
# Or try: "all-mpnet-base-v2", "sentence-transformers/all-MiniLM-L12-v2"
```

## 📊 Monitor Services

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f query-engine
docker-compose logs -f pdf-processor
docker-compose logs -f ollama
```

### Check Database Size

```bash
du -sh chroma_db/
ls -la pdf_uploads/
```

### View API Swagger Docs

- Processor: http://localhost:8000/docs
- Query Engine: http://localhost:8001/docs

## 🧹 Cleanup

### Clear Vector Database

```bash
# Via API
curl -X POST http://localhost:8000/clear

# Via Docker
docker-compose exec pdf-processor python -c "
import shutil
from pathlib import Path
if Path('chroma_db').exists():
    shutil.rmtree('chroma_db')
"
```

### Stop Services

```bash
docker-compose down
```

### Remove Everything

```bash
docker-compose down -v
rm -rf pdf_uploads chroma_db
```

## 🆘 Troubleshooting

### Services Won't Start

```bash
# Check Docker
docker ps

# Check logs
docker-compose logs

# Restart
docker-compose restart
```

### Model Download Fails

```bash
# Check Ollama container
docker logs pdf_pipeline_ollama

# Try manual download
docker exec -it pdf_pipeline_ollama /bin/bash
ollama pull mistral
exit
```

### Out of Memory

Reduce LLM model:
```bash
docker exec pdf_pipeline_ollama ollama pull orca-mini  # Smaller model
```

Or increase Docker memory limits in `docker-compose.yml`:
```yaml
services:
  query-engine:
    deploy:
      resources:
        limits:
          memory: 8G
```

### Slow Performance

1. Check available disk space: `df -h`
2. Clear Docker cache: `docker system prune`
3. Use smaller model: `orca-mini` or `neural-chat`
4. Reduce CHUNK_SIZE in pdf_processor.py

### CUDA/GPU Issues

If you have NVIDIA GPU and want GPU acceleration:

```bash
# Use NVIDIA CUDA image
# Modify docker-compose.yml Ollama service:
image: ollama/ollama:latest-gpu
```

## 📊 Available LLM Models

| Model | Size | Speed | Quality | Command |
|-------|------|-------|---------|---------|
| mistral | 4GB | Slow | Excellent | `ollama pull mistral` |
| neural-chat | 2.5GB | Fast | Good | `ollama pull neural-chat` |
| orca-mini | 1.3GB | Very Fast | Fair | `ollama pull orca-mini` |
| llama2 | 3.8GB | Slow | Excellent | `ollama pull llama2` |
| dolphin-mixtral | 26GB | Very Slow | Best | `ollama pull dolphin-mixtral` |

## 📚 API Reference

### Upload Endpoint

```
POST /upload
Content-Type: multipart/form-data

Response: {
  "filename.pdf": {
    "status": "success",
    "chunks": 42,
    "text_length": 15000
  }
}
```

### Query Endpoint

```
POST /query
Content-Type: application/json

Request: {
  "query": "Your question",
  "num_results": 3
}

Response: {
  "answer": "The answer to your question...",
  "sources": [
    {
      "source": "document.pdf",
      "chunk_index": 5,
      "content": "..."
    }
  ]
}
```

### Status Endpoints

```
GET /status
GET /health
GET /models
```

## 🎯 Best Practices

1. **Organize Documents** - Group related PDFs in collections
2. **Query Refinement** - Be specific with questions for better answers
3. **Monitor Performance** - Watch logs for bottlenecks
4. **Regular Backups** - Backup chroma_db directory
5. **Test Queries** - Test with simple questions first
6. **Chunk Size Tuning** - Adjust based on document type
7. **Model Selection** - Use smaller models for speed, larger for quality

## 📖 Example Workflows

### Basic Query Workflow

```bash
# 1. Start services
docker-compose up -d

# 2. Upload document
python cli.py --upload report.pdf

# 3. Ask questions
python cli.py --query "What are the main findings?"
```

### Batch Upload

```bash
python cli.py --upload *.pdf
```

### Interactive Session

```bash
python cli.py --interactive
# You: What is this about?
# Assistant: ...
# You: Tell me more about section 2
# Assistant: ...
# Type 'exit' to quit
```

## 🔗 Useful Links

- [Ollama Models](https://ollama.ai/library)
- [LangChain Docs](https://python.langchain.com)
- [Chroma Docs](https://docs.trychroma.com)
- [HuggingFace Models](https://huggingface.co/models)

---

**Need Help?** Check the logs: `docker-compose logs -f`
