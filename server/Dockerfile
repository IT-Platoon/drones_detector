FROM python:3.10.5-slim-buster

RUN apt-get update && \
    apt-get install --no-install-recommends -y libpq-dev build-essential libgl1-mesa-glx libglib2.0-0 python3-opencv ffmpeg && \
    apt-get clean

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY . /server
WORKDIR /server

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --with dev --no-interaction --no-ansi --no-root && \
    poetry cache clear . --all && \
    pip cache purge && \
    rm -r ~/.cache/pip && \
    rm -rf /root/.cache/pip
