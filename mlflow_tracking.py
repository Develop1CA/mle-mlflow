import mlflow
import os
import pandas as pd
from psycopg2 import connect
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# 1. Подключение к PostgreSQL и загрузка данных
connection = {
    "host": os.getenv("DB_DESTINATION_HOST"),
    "port": os.getenv("DB_DESTINATION_PORT"),
    "dbname": os.getenv("DB_DESTINATION_NAME"),
    "user": os.getenv("DB_DESTINATION_USER"),
    "password": os.getenv("DB_DESTINATION_PASSWORD")
}

with connect(**connection) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users_churn")
        data = cur.fetchall()
        columns = [col[0] for col in cur.description]

df = pd.DataFrame(data, columns=columns)

# 2. Сохранение артефактов
with open("columns.txt", "w", encoding="utf-8") as f:
    f.write(",".join(df.columns))

df.to_csv("users_churn.csv", index=False)

# 3. Настройка MLflow
EXPERIMENT_NAME = "churn_ivanov_ii"  # Например, "churn_ivanov"
RUN_NAME = "data_validation"

# Указываем URI сервера MLflow
mlflow.set_tracking_uri("http://localhost:5000")

# Создаем/получаем эксперимент
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
if experiment is None:
    experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
else:
    experiment_id = experiment.experiment_id

# 4. Логирование данных
with mlflow.start_run(experiment_id=experiment_id, run_name=RUN_NAME) as run:
    # Пример метрик (замените на ваши)
    stats = {
        "data_length": df.shape[0],
        "missing_values": df.isnull().sum().sum()
    }
    mlflow.log_metrics(stats)
    
    # Логируем артефакты
    mlflow.log_artifact("columns.txt", artifact_path="data")
    mlflow.log_artifact("users_churn.csv", artifact_path="data")

    print(f"Run ID: {run.info.run_id}")

# 5. Очистка
os.remove("columns.txt")
os.remove("users_churn.csv")