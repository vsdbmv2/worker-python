FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SERVER_URL=ws://192.168.0.25:4242
ENV WORKS_AMOUNT=2

CMD ["python", "main.py"]