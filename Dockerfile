FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir flask requests

EXPOSE 5000

CMD ["python", "core/api_server.py"]
