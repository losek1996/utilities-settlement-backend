ARG PYTHON_VERSION=3.14.0
ARG DEBIAN_VERSION=bookworm

FROM python:${PYTHON_VERSION}-slim-${DEBIAN_VERSION} AS base
ENV PYTHONUNBUFFERED 1
ENV PROJECT_DIR /project

# Install system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

ADD requirements.txt .
RUN pip install -r requirements.txt

WORKDIR $PROJECT_DIR/utilities_settlement_backend
ADD . $PROJECT_DIR