FROM python:3.13.7

WORKDIR /app

# Install system dependencies for PDF generation
RUN apt-get update && apt-get install -y \
    fonts-dejavu-core \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Use environment variable to control reload
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 ${RELOAD_FLAG:---reload}"]

