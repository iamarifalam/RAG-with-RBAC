# 🚀 Atlas: Enterprise Knowledge Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg)](https://www.docker.com/)
[![CI/CD](https://github.com/iamarifalam/RAG-with-RBAC/actions/workflows/ci.yml/badge.svg)](https://github.com/iamarifalam/RAG-with-RBAC/actions)

> **Secure, production-ready RAG system** with role-based access control for enterprise knowledge management. Built for companies that need to safely expose internal documents without data leaks.

## ✨ Why Atlas?

Traditional RAG systems generate answers then filter them. **Atlas is different** - it filters documents *before* retrieval, preventing information leakage at the source. This makes it:

- 🔒 **Unbreakable security** - No prompt injection can bypass role-based access
- ⚡ **Blazing fast** - Sub-100ms responses with BM25 search
- 📊 **Fully auditable** - Every query logged for compliance
- 🏢 **Enterprise-ready** - JWT auth, Prometheus metrics, Docker deployment

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Query    │ -> │     Auth        │ -> │   Guardrails    │ -> │   Retrieval     │
│                 │    │   (JWT)         │    │   (Pre-LLM)     │    │   (BM25)        │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
                                                                          │
                                                                          ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LLM Gen       │ -> │   Response      │ -> │   Audit Log     │ -> │   Metrics       │
│   (OpenAI/Mock) │    │   (Source Attr) │    │   (JSON)        │    │   (Prometheus)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/iamarifalam/RAG-with-RBAC.git
cd RAG-with-RBAC

# Install dependencies
uv sync --group dev

# Run locally
uv run uvicorn atlas_rag.main:app --reload --app-dir src --port 8002

# Or with Docker
docker-compose up -d
```

Visit `http://localhost:8002` and login with demo credentials.

## 🎯 Key Features

### 🔐 Security First
- **Role-based access control** at retrieval layer (not output filtering)
- **JWT authentication** with configurable token TTL
- **Guardrails** prevent hallucinations and information leaks
- **Audit trails** for compliance and investigations

### ⚡ Performance
- **Sub-second responses** with optimized BM25 search
- **Async processing** with FastAPI
- **Scalable architecture** ready for Kubernetes
- **Health monitoring** with Prometheus metrics

### 🛠️ Enterprise Ready
- **Docker containerization** for easy deployment
- **Structured logging** for ELK stack integration
- **Environment-based config** (dev/staging/prod)
- **Comprehensive testing** with pytest

## 🎮 Live Demo

Try Atlas with these demo users:

| Role | Username | Password | Access Level |
|------|----------|----------|--------------|
| 👨‍💼 Finance | `alice.finance` | `FinanceDemo123` | Finance docs + policies |
| 👩‍💼 HR | `harry.hr` | `HRDemo123` | HR docs + policies |
| 👔 Executive | `erin.exec` | `ExecDemo123` | All documents |
| 👤 Employee | `emma.employee` | `EmployeeDemo123` | Policies only |

**Test the security:** Login as `alice.finance` and ask "What's in the HR payroll policy?" → Access denied!

## 📡 API Endpoints

```bash
# Authentication
POST /api/auth/login
{
  "username": "alice.finance",
  "password": "FinanceDemo123"
}

# Query knowledge base
POST /api/chat
Authorization: Bearer <jwt_token>
{
  "question": "What is the Q3 budget?"
}

# Health check
GET /health

# Metrics (Prometheus)
GET /metrics
```

## 🛠️ Tech Stack

- **Backend**: Python 3.11, FastAPI, Pydantic
- **Search**: BM25 (rank_bm25), document chunking
- **Auth**: PyJWT, role-based permissions
- **LLM**: Pluggable (OpenAI, Groq, Azure OpenAI, Mock)
- **Monitoring**: Prometheus metrics, structured JSON logging
- **Deployment**: Docker, docker-compose, Kubernetes-ready
- **Testing**: pytest, coverage reporting
- **Dev Tools**: uv (package manager), ruff (linter), mypy (type checking)

## 📊 Sample Response

```json
{
  "answer": "Based on the Q3 budget document, the total allocated budget is $2.5M with the following breakdown: Engineering ($1.2M), Marketing ($0.8M), Operations ($0.5M).",
  "sources": [
    {
      "document": "finance_q3_budget.md",
      "chunk": "Q3 Total Budget: $2.5M. Engineering: $1.2M (48%). Marketing: $0.8M (32%). Operations: $0.5M (20%)."
    }
  ],
  "blocked_reason": null
}
```

## 🔧 Configuration

```env
# Core settings
APP_NAME=Atlas RAG Assistant
JWT_SECRET_KEY=your-secret-here
LLM_MODE=mock  # or openai_compatible

# OpenAI (if using real LLM)
OPENAI_COMPATIBLE_BASE_URL=https://api.openai.com/v1
OPENAI_COMPATIBLE_API_KEY=sk-your-key

# Search settings
MAX_CONTEXT_CHUNKS=4
MIN_RETRIEVAL_SCORE=0.08

# Security
ALLOWED_TOPICS=["finance", "hr", "marketing", "policy", "security"]
```

## 🧪 Development

```bash
# Install dev dependencies
uv sync --group dev

# Run tests with coverage
uv run pytest tests/ -v --cov=atlas_rag

# Format code
uv run ruff format src/ tests/

# Type check
uv run mypy src/

# Lint
uv run ruff check src/ tests/
```

## 📈 Monitoring

Atlas exports comprehensive metrics:

```bash
# Request metrics
requests_total{endpoint="chat",status="200"} 42
request_duration_p95{endpoint="chat"} 245ms

# Security metrics
guardrail_blocks{reason="domain_filter"} 5
auth_failures{reason="invalid_token"} 2

# System health
index_documents_total 4
uptime_seconds 3600
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Add tests for new functionality
4. Ensure all tests pass: `uv run pytest`
5. Format code: `uv run ruff format`
6. Commit changes: `git commit -m 'Add amazing feature'`
7. Push to branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

## 📄 License

Licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for secure enterprise knowledge management**

[⭐ Star this repo](https://github.com/iamarifalam/RAG-with-RBAC) if you find it useful!
