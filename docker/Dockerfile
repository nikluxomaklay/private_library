FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn


COPY ./entrypoint.sh .
COPY --exclude=config.yml ./src .
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
