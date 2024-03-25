FROM python:3.11.1-slim

WORKDIR /producer

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY producer/producer.py .

CMD ["python", "producer.py"]