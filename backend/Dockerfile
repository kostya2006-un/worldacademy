# Используем базовый образ с Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем общий файл requirements.txt из корневой директории проекта
COPY ../requirements.txt /requirements.txt
RUN apt-get update && apt-get install -y libpq-dev
# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /requirements.txt

# Копируем файлы приложения
COPY ./app /app

# Открываем порт, на котором работает FastAPI
EXPOSE 8000

# Команда для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
