# syntax=docker/dockerfile:1.7
# 1) Лёгкие правки поверх рабочего варианта
FROM mcr.microsoft.com/playwright/python:v1.54.0

# Чуть чище вывод/кеши pip
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 2) Java для Allure (headless — меньше весит) + уборка apt-кэша
RUN apt-get update \
 && apt-get install -y --no-install-recommends openjdk-17-jre-headless ca-certificates curl \
 && rm -rf /var/lib/apt/lists/*

# 3) Allure CLI (прикалываем в /usr/local/bin) + аккуратная распаковка
ARG ALLURE_VERSION=2.34.1
RUN set -eux; \
    curl -fsSL -o /tmp/allure.tgz "https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz"; \
    tar -xzf /tmp/allure.tgz -C /opt; \
    ln -sf /opt/allure-${ALLURE_VERSION}/bin/allure /usr/local/bin/allure; \
    rm /tmp/allure.tgz

# 4) Рабочая директория — остаётся как у тебя
WORKDIR /app

# 5) Сначала зависимости — лучше кешируется
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 6) Потом код проекта
COPY . .

# (опционально) дефолтная команда, если запускаешь контейнер вручную
# CMD ["pytest", "-n", "auto", "--alluredir=allure-results"]
