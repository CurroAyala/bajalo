FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y ffmpeg clamav && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir yt-dlp mutagen

RUN freshclam

COPY main.py .

ENTRYPOINT ["python", "/app/main.py"]