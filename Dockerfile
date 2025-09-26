FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/home/stockinc" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    stockinc

USER stockinc

ENTRYPOINT ["python3", "-m", "src.main"]
