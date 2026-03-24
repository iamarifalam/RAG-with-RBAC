FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY templates ./templates
COPY static ./static
COPY data ./data

RUN pip install --no-cache-dir uv \
    && uv pip install --system .

EXPOSE 8000

CMD ["uvicorn", "atlas_rag.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"]

