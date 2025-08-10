FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ADD --keep-git-dir=true https://github.com/nikluxomaklay/private_library.git .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "private_library.wsgi"]
