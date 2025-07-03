#!/bin/bash

# Создаём папку для хранения данных MLflow (если её нет)
mkdir -p mlflow_experiments_store

# Запускаем MLflow Tracking Server
mlflow server \
    --backend-store-uri file:./mlflow_experiments_store \
    --default-artifact-root file:./mlflow_experiments_store \
    --host 0.0.0.0 \
    --port 5000

echo "MLflow Tracking Server запущен. Доступен по адресу: http://localhost:5000"