FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

COPY . .

RUN find . -path "*/*.sqlite3" -delete

RUN cd src && \
    find . -path "*/migrations/*.py" -not -name "__init__.py" -delete && \
    find . -path "*/migrations/*.pyc" -delete

ENV DJANGO_ENV=production
ENV PYTHONUNBUFFERED=1

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
