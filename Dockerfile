FROM python:3.10-slim

# Install Tesseract OCR dan bahasa Indonesia
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-ind \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependensi dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh file aplikasi
COPY . .

# Jalankan aplikasi menggunakan Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]