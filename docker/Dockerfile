# syntax = docker/dockerfile
# * using loose versioning for now
# >>>
FROM python:3-alpine as setup-pybuild
# TODO: build from source code using poetry
# * shrink building size/cut dependencies

RUN --mount=type=cache,target=/var/cache/apk \
    --mount=type=cache,target=/var/lib/apk \
    --mount=type=cache,target=/etc/apk/cache \
    apk update && \
    apk add --update \
    # build tools
    git \
    make \
    # pip cryptography, lxml and yes: rust... 
    # python3-dev \
    # g++ \
    # wget \
    openssl-dev \
    libffi-dev \
    cargo \
    libxml2-dev \
    libxslt-dev \
    musl-dev \
    gcc \
    gfortran \
    build-base

# RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - # ! no poetry on $PATH
RUN --mount=type=cache,target=~/.cache/pip/ \
    pip install --upgrade pip \
    pip install poetry

RUN poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true

# >>>
FROM setup-pybuild as pybuild

COPY ./pyproject.toml /pyproject.toml
WORKDIR /code
# poetry.lock is ".dockerignore"d
RUN --mount=type=cache,target=/code \
    mv /pyproject.toml /code/pyproject.toml && \
    poetry lock

COPY . /code
RUN --mount=type=cache,target=/code/.venv \
    --mount=type=cache,target=~/.cache/pypoetry \
    make build-bin __POETRY_FLAGS=--no-dev

# >>>
# ! FROM scratch/setup-pybuild: not working (glibc related issue. idk)
# FROM scratch as bin
# FROM alpine as bin
FROM debian:buster-slim as bin
# FROM setup-pybuild as bin

COPY --from=pybuild /code/dist/pbivcs /bin/pbivcs
USER 1000:1000
ENTRYPOINT ["/bin/pbivcs"]
