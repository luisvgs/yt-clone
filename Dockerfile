FROM python:3.13.5-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV PYTHONPATH="/app"
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
