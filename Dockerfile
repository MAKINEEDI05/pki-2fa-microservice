FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/install -r requirements.txt

FROM python:3.11-slim
ENV TZ=UTC
RUN apt-get update && apt-get install -y cron tzdata && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN ln -sf /usr/share/zoneinfo/UTC /etc/localtime && echo "UTC" > /etc/timezone
WORKDIR /app
COPY --from=builder /install /usr/local/lib/python3.11/site-packages
COPY app/ app/
COPY scripts/ scripts/
COPY cron/ cron/
COPY student_private.pem student_private.pem
COPY student_public.pem student_public.pem
COPY instructor_public.pem instructor_public.pem
RUN mkdir -p /data /cron && chmod 755 /data /cron
RUN chmod 0644 cron/2fa-cron && crontab cron/2fa-cron
EXPOSE 8080
CMD service cron start && /usr/local/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8080
