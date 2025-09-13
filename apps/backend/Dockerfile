# apps/backend/Dockerfile
FROM python:3.10-slim as builder
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential libpq-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip wheel --no-cache-dir -r requirements.txt -w dist

FROM python:3.10-slim
WORKDIR /app
RUN addgroup --system app && adduser --system --ingroup app app
COPY --from=builder /app/dist /wheels
RUN pip install --no-cache /wheels/*
COPY app.py .
ENV FLASK_ENV=production
USER app
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "2", "--threads", "4"]
