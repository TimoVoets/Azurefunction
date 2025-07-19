FROM python:3.12-slim

# Systeempackages installeren voor pdf2image en tesseract
RUN apt-get update && \
    apt-get install -y tesseract-ocr poppler-utils && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Kopieer requirements en installeer Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieer de app code
COPY . .

# Start FastAPI via Gunicorn + Uvicorn workers
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app:app", "-b", "0.0.0.0:8000"]
