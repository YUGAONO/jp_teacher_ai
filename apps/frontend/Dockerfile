FROM python:3.13.7

WORKDIR /app

# 依存関係があれば requirements.txt を作ってここでCOPY
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0"]
