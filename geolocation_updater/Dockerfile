FROM python:3.11.8-alpine AS builder

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirments.txt

ENTRYPOINT [ "sh", "start.sh" ]