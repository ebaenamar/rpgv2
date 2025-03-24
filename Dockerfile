FROM python:3.9-slim

WORKDIR /app

# Install curl for healthchecks and dependencies for faiss-cpu
RUN apt-get update && apt-get install -y curl swig build-essential python3-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.docker.txt .
RUN pip install --no-cache-dir -r requirements.docker.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
