# Используем официальный Python 3.12
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Указываем переменную окружения для Django
ENV PYTHONPATH=/app

# Открываем порт для Django
EXPOSE 8000

RUN python manage.py collectstatic --noinput


# Запускаем сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
