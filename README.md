# 🧠 RAGForge

A modular **Retrieval-Augmented Generation (RAG)** application — a FastAPI backend that turns your documents into a searchable, question-answerable knowledge base, paired with a polished Streamlit UI on top of it.

```
┌──────────────────────────┐
│      Streamlit UI         │   Upload → Process → Index → Search → Chat
│  Modern RAG Dashboard     │
└────────────┬──────────────┘
             │ HTTP
             ▼
┌──────────────────────────┐
│      FastAPI Backend      │   Chunking, embeddings, retrieval, generation
└────────────┬──────────────┘
             ▼
┌──────────────────────────┐
│  MongoDB · Qdrant · LLM   │   Metadata · Vector index · OpenAI / Cohere
└──────────────────────────┘
```

## ✨ Features

- **Document upload & processing** — upload PDFs/text files per project, chunk them with configurable size/overlap
- **Vector indexing** — embed chunks and push them into a [Qdrant](https://qdrant.tech/) collection
- **Semantic search** — query the knowledge base and get back the most relevant chunks, ranked by similarity
- **RAG question answering** — ask natural-language questions and get answers grounded in your own documents
- **Pluggable LLM & embedding providers** — OpenAI and Cohere supported out of the box via a factory/provider pattern
- **Bilingual prompt templates** — English and Arabic RAG prompts (`src/stores/llm/templatess/locales`)
- **Streamlit dashboard** — a full product-style UI on top of the API: upload, process, index, search, and a ChatGPT-style RAG chat, all in one place

## 🎯 What this project demonstrates

- **Modular RAG architecture** built with the **Factory Design Pattern** — LLM and vector-DB providers are swappable behind `LLMInterface` / `VectorDBInterface`, with an end-to-end **LangChain + Hugging Face** pipeline for PDF ingestion, chunking, embedding generation, and retrieval
- **Asynchronous REST APIs** with **FastAPI**, **Pydantic** request/response schemas, **Motor** (async MongoDB driver), and **dependency injection** for document ingestion, querying, and chat — endpoints validated end-to-end with the bundled **Postman** collection
- **LLM + vector DB integration** — **Qdrant** and **MongoDB** working together with prompt engineering and conversation-aware context to generate grounded, source-aware RAG responses
- **Streamlit UI** for the full pipeline: document upload, processing, indexing, semantic search, and RAG chat
- **Dockerized** local infrastructure via `docker-compose` for reproducible setup

## 🏗️ Architecture

- **`src/`** — the FastAPI backend
  - `routes/` — API routes (`base`, `data`, `nlp`)
  - `controllers/` — business logic (upload validation, chunking, project/asset management)
  - `models/` — Mongo-backed data models and schemes (`Project`, `Asset`, `DataChunk`)
  - `stores/llm/` — LLM & embedding provider abstraction (`LLMInterface` + OpenAI/Cohere/HuggingFace providers)
  - `stores/vectordb/` — vector DB abstraction (`VectorDBInterface` + Qdrant provider)
- **`streamlit_app/`** — the Streamlit frontend, calling the backend purely over HTTP (no RAG logic duplicated on the UI side)
- **`docker/`** — `docker-compose.yaml` to run MongoDB locally

## 📦 Requirements

- Python 3.8+
- MongoDB (via Docker, or your own instance)
- An OpenAI and/or Cohere API key (or point `GENERATION_BACKEND` / `EMBEDDING_BACKEND` at whichever provider you configure)

## 🚀 Getting started

### 1. Clone & create an environment

```bash
git clone https://github.com/<your-username>/RAGForge.git
cd RAGForge

conda create -n ragforge python=3.8
conda activate ragforge
```

### 2. Start MongoDB

```bash
cd docker
cp .env.example .env      # set MONGO_INITDB_ROOT_USERNAME / PASSWORD
docker compose up -d
cd ..
```

### 3. Configure & run the backend

```bash
cd src
pip install -r requirements.txt

cp env.example .env
```

Fill in `.env` — at minimum:

| Variable | Description |
|---|---|
| `APP_NAME`, `APP_VERSION` | App metadata returned by the health endpoint |
| `FILE_ALLOWED_TYPES` | Allowed upload MIME types, e.g. `["application/pdf","text/plain"]` |
| `FILE_MAX_SIZE` | Max upload size in MB |
| `FILE_DEFAULT_CHUNK_SIZE` | Byte-read chunk size for streaming uploads |
| `MONGODB_URL`, `MONGODB_DATABASE` | Mongo connection string & DB name |
| `GENERATION_BACKEND` / `EMBEDDING_BACKEND` | `OPENAI` and/or `COHERE` |
| `OPENAI_API_KEY` / `COHERE_API_KEY` | Provider API keys |
| `GENERATION_MODEL_ID` / `EMBEDDING_MODEL_ID` / `EMBEDDING_MODEL_SIZE` | Model selection |
| `VECTOR_DB_BACKEND`, `VECTOR_DB_PATH`, `VECTOR_DB_DISTANCE_METHOD` | Qdrant config (local, file-based by default) |
| `PRIMARY_LANG`, `DEFAULT_LANG` | RAG prompt template locale (`en` / `ar`) |

Run the API:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Verify it's up:

```bash
curl http://127.0.0.1:8000/api/v1/
# {"app_name":"RAGForge","app_version":"0.1"}
```

A ready-to-import [Postman collection](src/assets/mini-rag-app.postman_collection.json) is included for exploring the API directly.

### 4. Run the Streamlit UI

In a second terminal:

```bash
cd streamlit_app
pip install -r requirements.txt

cp .env.example .env      # point API_BASE_URL at your backend if not localhost:8000

streamlit run app.py
```

Open the URL Streamlit prints (default `http://localhost:8501`) and walk through the pipeline: **Upload → Process → Index → Search → Chat**.

See [`streamlit_app/README.md`](streamlit_app/README.md) for UI-specific details and the full endpoint mapping.

## 🔌 API reference

All routes are mounted under `/api/v1` and scoped to a `project_id` path parameter.

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/v1/` | Health check |
| `POST` | `/api/v1/data/upload/{project_id}` | Upload a document |
| `POST` | `/api/v1/data/process/{project_id}` | Chunk uploaded file(s) |
| `POST` | `/api/v1/nlp/index/push/{project_id}` | Embed chunks & push into the vector index |
| `GET` | `/api/v1/nlp/index/info/{project_id}` | Vector collection metadata |
| `POST` | `/api/v1/nlp/index/search/{project_id}` | Semantic search |
| `POST` | `/api/v1/nlp/index/answer/{project_id}` | RAG question answering |

## 🛠️ Tech stack

**Backend:** FastAPI · Pydantic · Motor (async MongoDB) · Dependency Injection · Factory Design Pattern · LangChain · Hugging Face · Qwen2.5-1.5B-Instruct · Qdrant · MongoDB · PyMuPDF · OpenAI / Cohere SDKs · Prompt Engineering · Conversation Memory · Postman
**Frontend:** Streamlit · Requests
**DevOps:** Docker

## 📄 License

See [LICENSE.txt](LICENSE.txt).

## 👤 Author

**Ehab Ashraf** — AI/ML Engineer (NLP, RAG, Agentic AI)
[GitHub](https://github.com/EhabAshraf32) · [LinkedIn](www.linkedin.com/in/ehab-ashraf-bba739176)
