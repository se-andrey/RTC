FROM python:3.11.1-slim

WORKDIR /consumer

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY consumer/consumer.py .

CMD ["python", "consumer.py"]