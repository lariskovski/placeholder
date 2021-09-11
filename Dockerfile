FROM alpine:3.13

WORKDIR /src

RUN apk add --no-cache  \
    python3             \
    py3-pip             \
    python3-dev         \
    libevent-dev        \
    make                \
    musl-dev            \
    libffi-dev          \
    gcc                 \
    ffmpeg

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY src/ .

CMD ["python3", "/src/app.py"]