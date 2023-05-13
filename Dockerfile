FROM alpine:3.13

WORKDIR /src

RUN apk add --no-cache  \
    libevent-dev        \
    python3-dev         \
    build-base          \
    libffi-dev          \
    musl-dev            \
    python3             \
    py3-pip             \
    ffmpeg              \
    make                \
    gcc

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY src/ .

CMD ["python3", "-u", "/src/app.py"]