#!/bin/bash

# Загружаем переменные окружения из .env
export $(cat .env | xargs)

# Устанавливаем переменные окружения для S3 и MLflow
export MLFLOW_S3_ENDPOINT_URL=https://storage.yandexcloud.net
export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
export AWS_BUCKET_NAME=$S3_BUCKET_NAME

# Запуск MLflow Tracking Server
mlflow server \
  --backend-store-uri postgresql://$DB_DESTINATION_USER:$DB_DESTINATION_PASSWORD@$DB_DESTINATION_HOST:$DB_DESTINATION_PORT/$DB_DESTINATION_NAME \
  --default-artifact-root s3://$AWS_BUCKET_NAME \
  --no-serve-artifacts