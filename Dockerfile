# 1. Используем официальный образ Playwright
FROM mcr.microsoft.com/playwright/python:v1.54.0

# 2. Устанавливаем Java для Allure
RUN apt-get update && apt-get install -y default-jre

# 3. Устанавливаем Allure Commandline
ARG ALLURE_VERSION=2.34.1
RUN curl -sSL "https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz" -o allure.tgz && \
    tar -zxvf allure.tgz -C /opt && \
    rm allure.tgz && \
    ln -s /opt/allure-${ALLURE_VERSION}/bin/allure /usr/bin/allure

# 4. Устанавливаем рабочую директорию
WORKDIR /app

# 5. Копируем и устанавливаем Python-зависимости
COPY requirements.txt .
RUN pip install -r requirements.txt

# 6. Копируем остальной код проекта
COPY . .