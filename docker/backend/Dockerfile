# pull official base image
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
  python3-dev \
  gcc \
  libc-dev \
  && rm -rf /var/lib/apt/lists/*

# RUN apk update && apk add python3-dev gcc libc-dev

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install gunicorn
ADD ./backend/requirements.txt /app/
RUN pip install -r /app/requirements.txt
RUN pip install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cpu

ADD ./backend /app/backend
ADD ./docker /app/docker

RUN chmod +x /app/docker/backend/server-entrypoint.sh
RUN chmod +x /app/docker/backend/worker-entrypoint.sh
RUN chmod +x /app/docker/backend/beat-entrypoint.sh
