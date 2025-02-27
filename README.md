## Описание проекта

Проект представляет собой RESTful сервис для управления библиотечным фондом. Система позволяет отслеживать наличие книг, выдачу книг читателям и контроль за возвратом книг. Основные функции включают создание, чтение, обновление и удаление (CRUD) записей о книгах, читателях и выдачах.

### Стек технологий

- Flask
- Gunicorn
- SQLAlchemy
- Alembic
- PostgreSQL
- psycopg2 
- pytest

## Установка и развертывание

### Предварительные требования

- Установленный Python (версия 3.6 и выше)
- Установленный PostgreSQL
- Менеджер зависимостей, `pip`

### Шаги по установке

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/artanastasion/library_flask_app
   ```

2. **Создайте и активируйте виртуальное окружение:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # На Windows используйте venv\Scripts\activate
   ```

3. **Установите зависимости:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте базу данных:**

   - Создайте базу данных в PostgreSQL.
   - Настройте строку подключения в файлах ```config.py, tests/book_tests.py, alembic.ini```

5. **Примените миграции базы данных:**

   ```bash
   alembic upgrade head
   ```

6. **Запустите приложение:**

   ```bash
    gunicorn -w 4 -b 127.0.0.1:5000 run:app
   ```

## Использование

### Эндпоинты

- **GET /api/books** - Получить список всех книг
- **POST /api/books** - Добавить новую книгу
- **PUT /api/books/{id}** - Обновить информацию о книге
- **DELETE /api/books/{id}** - Удалить книгу
  
- **GET /api/readers** - Получить список всех читателей
- **POST /api/readers** - Добавить нового читателя
- **PUT /api/readers/{id}** - Обновить информацию о читателе
- **DELETE /api/readers/{id}** - Удалить читателя

- **GET /api/issuances** - Получить список всех выдач
- **POST /api/issuances** - Добавить новую выдачу
- **PUT /api/issuances/{id}** - Обновить информацию о выдаче
- **DELETE /api/issuances/{id}** - Удалить выдачу


- **GET /api/publishers** - Получить список всех издательств
- **POST /api/publishers** - Добавить новое издательство
- **PUT /api/publishers/{id}** - Обновить информацию о издетельстве
- **DELETE /api/publishers/{id}** - Удалить издательство

- **GET /api/report?date=YYYY-MM-DD** - Сгенерировать отчет о должниках на указанную дату


## Генерация фикстур

Скрипт для генерации фикстур в базу данных можно запустить следующим образом:

```bash
python scripts/fixtures.py
```
