FROM python:3.11.8-alpine AS builder

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirments.txt

EXPOSE 8000

CMD ["uvicorn", "url_shortener.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--use-colors", "--no-server-header", "--no-date-header"]