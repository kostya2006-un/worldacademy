# Используем базовый образ с Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /bot

# Копируем общий файл requirements.txt из корневой директории проекта
COPY ../requirements.txt /requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /requirements.txt

# Копируем файлы Telegram-бота
COPY ./bot /bot

# Команда для запуска бота
CMD ["python", "main.py"]
