FROM python:3.11-slim

WORKDIR /app

# System deps kept minimal for a small image
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Only copy what the API needs at runtime (not the whole DVC/MLflow project)
COPY src/app.py src/app.py
COPY models/model.pkl models/model.pkl
COPY models/label_encoders.pkl models/label_encoders.pkl

ENV MODEL_PATH=models/model.pkl
ENV ENCODERS_PATH=models/label_encoders.pkl
ENV PORT=8000

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
