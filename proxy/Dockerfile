FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV MASTER_KEY=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
ENV API_KEYS=demo-key-123
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
