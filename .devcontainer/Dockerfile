FROM mcr.microsoft.com/devcontainers/python:3.14

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    SAL_USE_VCLPLUGIN=svp

# LibreOffice (headless) for converting documents to PDF.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libreoffice \
        fonts-liberation \
        fonts-dejavu-core \
        fontconfig \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
