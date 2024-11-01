FROM python:3.10-buster

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем requirements.txt для установки зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем исходный код приложения и файл модели
COPY entropy.py .
COPY app.py .
COPY pipeline.joblib .

EXPOSE 8000

# Start the FastAPI application using the specified port from environment variables
CMD ["python", "app.py"]
