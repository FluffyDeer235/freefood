FROM python:3.12-slim

# Prevent python from buffering stdout, stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD []
