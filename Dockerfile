# Gebruik een slanke Python-basis
FROM python:3.12-slim

# Installeer systeemdependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr poppler-utils && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Werkdirectory
WORKDIR /app

# Vereisten kopiëren & installeren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App kopiëren
COPY app.py .

# Start de server met meerdere workers
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app:app", "-b", "0.0.0.0:8000"]
