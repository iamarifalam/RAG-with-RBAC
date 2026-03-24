# Atlas: Enterprise Knowledge Assistant

A secure RAG system for internal company knowledge. Like Google for your docs, but with role-based access control and audit trails.

## Quick Start

```bash
# Clone and setup
git clone https://github.com/iamarifalam/RAG-with-RBAC.git
cd RAG-with-RBAC
uv sync --group dev

# Run locally
uv run uvicorn atlas_rag.main:app --reload --app-dir src --port 8002

# Or with Docker
docker-compose up -d
```

Open http://localhost:8002 and login with demo credentials.

## What Makes Atlas Different

- **Security at the source**: Filters documents before retrieval, not after generation
- **Role-based access**: Finance sees finance docs, HR sees HR docs
- **Guardrails**: Prevents hallucinations and information leaks
- **Full audit trail**: Every query logged for compliance
- **Source attribution**: Always shows where answers come from

## Demo Users

| Role | Username | Password | Access |
|------|----------|----------|--------|
| Finance | alice.finance | FinanceDemo123 | Finance + policies |
| HR | harry.hr | HRDemo123 | HR + policies |
| Executive | erin.exec | ExecDemo123 | All documents |
| Employee | emma.employee | EmployeeDemo123 | Policies only |

## Architecture

```
User Query → Auth → Guardrails → Retrieval → LLM → Response
     ↓         ↓         ↓         ↓         ↓         ↓
   JWT      RBAC     Domain    BM25     OpenAI    Audit
   Token    Check    Filter   Search    Gen      Logs
```

### Key Components

- **Auth**: JWT tokens with role claims
- **Guardrails**: Pre-LLM checks for domain, relevance, sensitivity
- **Retrieval**: BM25 search over indexed documents
- **LLM**: Pluggable backends (mock, OpenAI, etc.)
- **Monitoring**: Prometheus metrics, structured logging

## API Endpoints

- `GET /health` - System status
- `POST /api/auth/login` - Get JWT token
- `POST /api/chat` - Ask questions (requires auth)
- `GET /api/admin/stats` - Usage stats (admin only)

## Configuration

Copy `.env.example` to `.env` and customize:

```env
JWT_SECRET_KEY=your-secret-here
ALLOWED_TOPICS=["finance", "hr", "marketing", "policy", "security"]
OPENAI_API_KEY=sk-your-key
LOG_LEVEL=INFO
```

## Deployment

### Docker (Recommended)

```bash
docker-compose up -d
```

### Manual

```bash
uv sync
uv run uvicorn atlas_rag.main:app --host 0.0.0.0 --port 8002
```

### Production

- Use reverse proxy (nginx/caddy)
- Set up monitoring (Prometheus/Grafana)
- Configure log aggregation
- Enable HTTPS

## Development

```bash
# Install dev dependencies
uv sync --group dev

# Run tests
uv run pytest tests/ -v

# Format code
uv run ruff format src/ tests/

# Type check
uv run mypy src/
```

## Security Notes

- JWT tokens expire in 1 hour
- All queries are logged
- Documents are filtered by user role before retrieval
- Guardrails prevent sensitive information leaks
- No external API calls in demo mode

## Contributing

1. Fork the repo
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a PR

## License

MIT - see LICENSE file for details.
