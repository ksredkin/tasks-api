# TasksAPI + Telegram Bot

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Aiogram](https://img.shields.io/badge/aiogram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=for-the-badge&logo=poetry&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-00A98F?style=for-the-badge&logo=alembic&logoColor=white)
![Unit Testing](https://img.shields.io/badge/Unit_Testing-4CAF50?style=for-the-badge&logo=testcafe&logoColor=white)

**TasksAPI** – это REST API для управления задачами с аутентификацией JWT, миграциями базы данных и современной архитектурой на FastAPI.  
**Telegram Bot** – интерфейс для взаимодействия с API через Telegram, позволяющий удобно создавать, редактировать и отслеживать задачи, папки, прогресс и статистику.

---

## 🎯 Возможности

### API
- ✅ Полноценная JWT-аутентификация (регистрация, вход, защита эндпоинтов)
- ✅ CRUD для задач, папок (с вложенностью) и пользователей
- ✅ Поддержка повторяющихся задач (daily/weekly/monthly с указанием времени)
- ✅ Поля `due_date` (дедлайн) и `visible_from` (видимость с даты)
- ✅ Статистика по задачам и папкам
- ✅ Миграции через Alembic
- ✅ Контейнеризация Docker
- ✅ Логирование всех операций
- ✅ Полное покрытие тестами (репозитории, сервисы, API)

### Telegram Bot
- 🤖 Удобный интерфейс с инлайн- и реплай-клавиатурами
- 🔑 Регистрация и вход по логину/паролю (с защитой от брутфорса)
- 📁 Создание, редактирование и удаление папок (с поддержкой вложенности)
- 📝 Создание, редактирование, удаление задач
- 🔁 Настройка повторения задач (интервал в минутах, daily/weekly/monthly)
- 📅 Команда `/today` – задачи на сегодня
- 📊 Команда `/stats` – статистика (общая и по папкам)
- 🚀 Импорт задач из текстового списка (`/import_tasks`)
- ⏲️ Таймер (`/timer`) и защита от брутфорса на стороне бота
- 🖼️ Кеширование фото для быстрого ответа

---

## 📁 Структура проекта

```
.
├── bot/                           # Telegram Bot
│   ├── app.py                     # Точка входа бота
│   ├── bot/                       # Исходный код бота
│   │   ├── core/
│   │   │   └── config.py          # Конфигурация (токен, параметры)
│   │   ├── database/              # Модели БД бота (если используются)
│   │   │   ├── connection.py
│   │   │   └── orm_models.py
│   │   ├── handlers/              # Обработчики aiogram
│   │   │   ├── callback.py
│   │   │   ├── commands.py
│   │   │   └── messages.py
│   │   ├── images/                # Статические изображения
│   │   │   └── bot_photo.jpeg
│   │   ├── keyboards/             # Клавиатуры (inline/reply)
│   │   │   └── inline.py
│   │   ├── messages/              # Текстовые сообщения (по модулям)
│   │   │   ├── auth.py
│   │   │   ├── common.py
│   │   │   ├── folders.py
│   │   │   └── tasks.py
│   │   ├── services/              # Фоновые сервисы (например, обработка повторений)
│   │   │   └── update_tasks_service.py
│   │   ├── states/                # Состояния FSM
│   │   │   ├── folder_states.py
│   │   │   ├── task_states.py
│   │   │   └── user_states.py
│   │   └── utils/                  # Утилиты
│   │       ├── api_client.py       # Клиент для API
│   │       ├── attempts_storage.py # Защита от брутфорса
│   │       ├── auth_storage.py     # Хранение токенов в памяти
│   │       ├── env_config.py       # Чтение .env
│   │       ├── helpers.py          # Вспомогательные функции
│   │       ├── logger.py           # Логирование
│   │       └── photo_cache.py      # Кеш file_id фотографий
│   ├── Dockerfile
│   ├── .env.example
│   ├── logs/                        # Логи бота
│   └── pyproject.toml                # Зависимости (Poetry)
│
├── tasks_api/                       # FastAPI приложение
│   ├── alembic/                      # Миграции Alembic
│   ├── alembic.ini
│   ├── app.py                         # Точка входа API
│   ├── Dockerfile
│   ├── .env.example
│   ├── logs/                           # Логи API
│   ├── tasks_api/                       # Основной код
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── folders_router.py
│   │   │       ├── tasks_router.py
│   │   │       └── user_router.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── database/
│   │   │   ├── connection.py
│   │   │   └── orm_models.py           # Модели SQLAlchemy (User, Folder, Task)
│   │   ├── models/
│   │   │   └── schemas.py               # Pydantic модели
│   │   ├── repositories/                 # Репозитории (SQLAlchemy)
│   │   │   ├── orm_folder_repository.py
│   │   │   ├── orm_task_repository.py
│   │   │   └── orm_user_repository.py
│   │   ├── services/                      # Бизнес-логика
│   │   │   ├── auth_service.py
│   │   │   └── user_service.py
│   │   └── utils/                          # Утилиты API
│   │       ├── attempts_storage.py
│   │       ├── check_database.py
│   │       ├── env_config.py
│   │       ├── helpers.py
│   │       ├── jwt.py
│   │       ├── logger.py
│   │       └── response_factory.py
│   └── tests/                              # Тесты
│       ├── run_tests.py
│       └── test_*.py
│
├── docker-compose.yml                      # Оркестрация всех сервисов
├── docs/
│   └── README.md
├── .gitignore
```

---

## 🚀 Установка и запуск через Docker

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/ksredkin/tasks-api.git
cd tasks-api
```

### 2. Установите Docker и Docker Compose (если ещё не установлены)
Следуйте [официальной инструкции](https://docs.docker.com/get-docker/).

### 3. Настройте переменные окружения

Скопируйте примеры файлов `.env` для каждого сервиса:

**Для API:**
```bash
cp tasks_api/.env.example tasks_api/.env
```

**Для бота:**
```bash
cp bot/.env.example bot/.env
```

Заполните их реальными данными. Ниже приведены примеры с пояснениями.

#### `tasks_api/.env`
```env
# Секретный ключ для JWT (минимум 32 символа)
SECRET_KEY = "your_super_secret_key_here_must_be_at_least_32_ch@rs"

# Ключ для защиты фоновых эндпоинтов (например, для активации повторяющихся задач)
API_KEY = "your_ultra_secret_api_key"

# Настройки подключения к PostgreSQL (внутри Docker сети)
DB_HOST = "postgres"
DB_PORT = 5432
DB_NAME = "tasks_db"
DB_USER = "postgres"
DB_PASSWORD = "123"
```

#### `bot/.env`
```env
# Токен Telegram бота (получить у @BotFather)
TOKEN = "7305379115:OEfc-V7M32-fELa38GhO5wVo8PDzQJ42AB2"

# Настройки подключения к API
API_HOST = "api"           # имя сервиса в docker-compose
API_PORT = 8000
API_KEY = "your_ultra_secret_api_key"   # должен совпадать с API_KEY в tasks_api/.env
```

### 4. Запустите все сервисы
```bash
docker-compose up --build
```

После успешного запуска будут доступны:
- **API**: http://localhost:8000
- **Документация Swagger**: http://localhost:8000/docs
- **Telegram Bot**: активен и готов к работе (напишите ему `/start`)

Для остановки: `docker-compose down`

---

## 📡 Использование API

### Публичные эндпоинты (без аутентификации)

#### Регистрация
```http
POST /user/register/
Content-Type: application/json

{
  "login": "my_login",
  "password": "my_password"
}
```

#### Вход
```http
POST /user/login/
Content-Type: application/json

{
  "login": "my_login",
  "password": "my_password"
}
```
**Ответ:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Защищенные эндпоинты (требуют Bearer токен)

**Заголовок:**
```
Authorization: Bearer <access_token>
```

#### Работа с папками
- `GET /folders/` – список папок пользователя
- `POST /folders/` – создать папку (тело: `{"name": "Название", "parent_id": null}`)
- `PUT /folders/{id}` – обновить папку
- `DELETE /folders/{id}` – удалить папку

#### Работа с задачами
- `GET /tasks/` – все задачи (поддерживает фильтры: `folder_id`, `state`, `due_date_from`, `due_date_to`)
- `GET /tasks/today` – задачи на сегодня (по полю `due_date`)
- `GET /tasks/stats` – статистика (общая и по папкам)
- `POST /tasks/` – создать задачу (подробнее см. схему)
- `PUT /tasks/{id}` – обновить задачу
- `DELETE /tasks/{id}` – удалить задачу

**Пример создания задачи с повторением:**
```json
{
  "title": "Ежедневная пробежка",
  "description": "в 7 утра",
  "folder_id": 1,
  "due_date": "2026-03-09T07:00:00",
  "visible_from": "2026-03-09T00:00:00",
  "recurrence_type": "daily",
  "recurrence_time": "07:00"
}
```

---

## 🤖 Использование Telegram бота

### Начало работы
Напишите боту команду `/start`. Бот предложит зарегистрироваться или войти.

### Доступные команды
```
📋 Доступные команды:
/start - 👋 Приветствие
/login - 🔑 Войти в аккаунт
/login {login} {password} - 🔑 Быстрый вход
/register - 🔒️ Создать аккаунт и войти
/logout - 🚫 Выйти из аккаунта
/tasks - 📃 Все задачи
/today - 📅 Задачи на сегодня
/done - 📜 Выполненные задачи
/create_task - 📝 Создать задачу
/import_tasks - 🚀 Импортировать задачи
/create_folder - 📁 Создать папку
/update_folder - 🔄 Обновить папку
/delete_folder - 🚫 Удалить папку
/stats - 📊 Статистика
/help - ❓️ Справка
```

### Инлайн-клавиатуры
- При просмотре списка задач каждая задача отображается в виде инлайн-кнопки с названием и датой.
- При нажатии на задачу открывается карточка с полным описанием и кнопками: ✅ Готово, 🔄 Обновить, ❌ Удалить, ⬅️ Назад.
- Аналогично для папок.

### Защита от брутфорса
- На стороне бота: после 10 неудачных попыток входа пользователь блокируется на день.
- На стороне API: ограничение на день через 5 неверных попыток.

---

## 🗄️ Миграции базы данных (Alembic)

При первом запуске API через Docker Compose миграции применяются автоматически. Для ручного управления:

```bash
docker exec -it tasks-api-api-1 bash   # имя контейнера может отличаться
alembic upgrade head
```

Новые миграции создаются командой:
```bash
alembic revision --autogenerate -m "описание"
```

## ⚙️ Архитектура и используемые технологии

### API
- **FastAPI** – высокопроизводительный веб-фреймворк
- **SQLAlchemy** + **Alembic** – ORM и миграции
- **Pydantic** – валидация данных
- **JWT** – аутентификация
- **PostgreSQL** – база данных
- **SlowAPI** – ограничение скорости запросов
- **Docker** – контейнеризация
- **Poetry** – управление зависимостями

### Бот
- **Aiogram 3.x** – асинхронный фреймворк для Telegram Bot API
- **FSM (Finite State Machine)** – управление диалогами
- **httpx** – асинхронные запросы к API
- **Собственное хранилище токенов** в памяти (словарь)
- **Защита от брутфорса** на основе попыток входа
- **Кеширование file_id** для ускорения отправки фото

---

## 📝 Примеры использования

### Создание задачи через бота
1. Введите `/create_task`.
2. Введите название.
3. Введите описание (или пропустите).
4. Выберите тип повторения (нет, ежедневно, еженедельно, ежемесячно).
5. При необходимости укажите время, день недели или число месяца.
6. Задача создана!

### Просмотр статистики
Введите `/stats`. Бот покажет:
- Всего задач
- Выполнено (в процентах)
- Активных
- Статистику по каждой папке (сколько задач, сколько выполнено, процент выполнения)

---

## 🤝 Вклад в проект

Если вы нашли ошибку или хотите предложить улучшение, создайте issue или pull request на GitHub.

---

⭐ Если проект оказался полезным, поставьте звезду на GitHub – это мотивирует развивать его дальше!