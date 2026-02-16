# 📋 TasksAPI

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=for-the-badge&logo=poetry&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-9C27B0?style=for-the-badge&logo=python&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![REST API](https://img.shields.io/badge/REST_API-FF6B6B?style=for-the-badge&logo=api&logoColor=white)
![Unit Testing](https://img.shields.io/badge/Unit_Testing-4CAF50?style=for-the-badge&logo=testcafe&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-00A98F?style=for-the-badge&logo=alembic&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

REST API для управления задачами с аутентификацией JWT, миграциями базы данных, логированием и современной архитектурой на FastAPI.  
REST API для управления задачами с аутентификацией JWT, миграциями базы данных, логированием и современной архитектурой на FastAPI.  

## 🎯 Особенности

- **Аутентификация JWT**: Защищенные эндпоинты с Bearer токенами
- **Полное CRUD**: Создание, чтение, обновление и удаление задач
- **ORM SQLAlchemy**: Современная работа с базой данных
- **Миграции Alembic**: Управление версиями схемы базы данных
- **Контейнеризация Docker**: Лёгкий запуск в изолированном окружении
- **Контейнеризация Docker**: Лёгкий запуск в изолированном окружении
- **Структурированная архитектура**: Четкое разделение на слои (API, сервисы, репозитории, модели)
- **Логирование**: Детальное логирование всех операций в отдельные файлы
- **Тестирование**: Полноценные unit-тесты с использованием временной БД
- **Безопасность**: Хранение чувствительных данных в .env файле
- **Валидация данных**: Pydantic модели для всех запросов и ответов
- **Поддержка PostgreSQL**: Надежная и масштабируемая база данных

## 📁 Структура проекта

```
tasks-api/
├── alembic/                  # Миграции базы данных (Alembic)
│   ├── versions/            # Файлы миграций
│   ├── env.py               # Конфигурация среды Alembic
│   └── script.py.mako       # Шаблон для генерации миграций
├── alembic.ini              # Конфигурация Alembic
├── docker-compose.yml       # Оркестрация контейнеров (FastAPI + PostgreSQL)
├── Dockerfile               # Сборка образа приложения
├── docker-compose.yml       # Оркестрация контейнеров (FastAPI + PostgreSQL)
├── Dockerfile               # Сборка образа приложения
├── docs/
│   └── README.md
├── .env                     # Конфигурация (не в репозитории)
├── .env.example             # Пример конфигурации
├── .gitignore
├── poetry.lock
├── pyproject.toml
├── app.py                   # Точка входа приложения
├── tasks_api/
│   ├── main.py             # Основное приложение FastAPI
│   ├── core/
│   │   └── config.py       # Конфигурация приложения
│   ├── database/           # Модуль работы с базой данных
│   │   ├── connection.py   # Управление соединением с БД через SQLAlchemy
│   │   └── orm_models.py   # Модели SQLAlchemy
│   │   └── orm_models.py   # Модели SQLAlchemy
│   ├── models/             # Pydantic модели для API
│   │   └── schemas.py      # Pydantic модели
│   │   └── schemas.py      # Pydantic модели
│   ├── api/
│   │   └── routes/
│   │       ├── tasks_router.py  # Маршруты для задач
│   │       └── user_router.py   # Маршруты для пользователей
│   ├── services/
│   │   ├── auth_service.py      # Сервис аутентификации
│   │   └── user_service.py      # Сервис пользователей
│   ├── repositories/
│   │   ├── orm_tasks_repository.py  # Репозиторий задач (SQLAlchemy)
│   │   └── orm_user_repository.py   # Репозиторий пользователей (SQLAlchemy)
│   └── utils/
│       ├── check_database.py    # Утилита проверки БД
│       ├── env_config.py        # Загрузка конфигурации
│       ├── jwt.py               # Работа с JWT токенами
│       ├── logger.py            # Настройка логгера
│       └── response_factory.py  # Фабрика ответов API
├── tests/
│   ├── run_tests.py        # Скрипт запуска всех тестов
│   ├── test_auth_service.py # Тесты сервиса аутентификации
│   ├── test_env_config.py   # Тесты конфигурации
│   ├── test_tasks_api.py    # Тесты API задач
│   ├── test_migrations.py   # Тест миграций
│   ├── test_migrations.py   # Тест миграций
│   ├── test_orm_repositories.py # Тесты репозиториев
│   └── test_user_service.py # Тесты сервиса пользователей
└── logs/                   # Директория для логов (не в репозитории)
```

## 🚀 Установка и запуск

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/ksredkin/tasks-api.git
cd tasks-api
```

### 2. Установите Docker и Docker Compose
- **Docker**: [Инструкция для вашей ОС](https://docs.docker.com/get-docker/)
- **Docker Compose**: обычно входит в состав Docker Desktop, либо устанавливается отдельно (см. [документацию](https://docs.docker.com/compose/install/))

Проверьте установку:
### 2. Установите Docker и Docker Compose
- **Docker**: [Инструкция для вашей ОС](https://docs.docker.com/get-docker/)
- **Docker Compose**: обычно входит в состав Docker Desktop, либо устанавливается отдельно (см. [документацию](https://docs.docker.com/compose/install/))

Проверьте установку:
```bash
docker --version
docker-compose --version
docker --version
docker-compose --version
```

### 3. Настройте окружение
### 3. Настройте окружение
```bash
# Скопируйте пример конфигурации
cp .env.example .env

# Отредактируйте .env файл при необходимости
# По умолчанию параметры уже настроены для работы в Docker
# Отредактируйте .env файл при необходимости
# По умолчанию параметры уже настроены для работы в Docker
```

**Пример содержимого `.env` файла:**
```env
# Секретный ключ для JWT (минимум 32 символа)
SECRET_KEY = "your_super_secret_key_here_must_be_at_least_32_ch@rs"

# Настройки подключения к PostgreSQL (для Docker-сети используйте имя сервиса)
DB_HOST = "postgres"          # Имя сервиса PostgreSQL в docker-compose.yml
# Настройки подключения к PostgreSQL (для Docker-сети используйте имя сервиса)
DB_HOST = "postgres"          # Имя сервиса PostgreSQL в docker-compose.yml
DB_PORT = 5432
DB_NAME = "tasks_db"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
```

### 4. Запустите приложение через Docker Compose
```bash
docker-compose build
docker-compose up
```

После сборки и запуска будут доступны:
- **API**: http://localhost:8000
- **Документация Swagger**: http://localhost:8000/docs
- **База данных PostgreSQL**: `localhost:5432` (логин/пароль из .env)

Для остановки: `docker-compose down`

### 5. Альтернативный запуск (без Docker, через Poetry)
Если вы хотите запустить приложение локально (без контейнеров), выполните:
```bash
poetry install
poetry install
poetry run python app.py
```
При этом PostgreSQL должен быть установлен и настроен отдельно.
При этом PostgreSQL должен быть установлен и настроен отдельно.

### 🔓 Публичные эндпоинты (без аутентификации)

#### Регистрация пользователя
```http
POST /user/register/
Content-Type: application/json

{
  "login": "string",
  "password": "string"
}
```

**Пример ответа:**
```json
{
  "login": "string",
  "id": 53
}
```

#### Вход пользователя
```http
POST /user/login/
Content-Type: application/json

{
  "login": "string",
  "password": "string"
}
```

**Пример ответа:**
```json
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
}
```

### 🔒 Защищенные эндпоинты (требуют JWT токен)

**Заголовок для аутентификации:**
```http
Authorization: Bearer {access_token}
```

#### Получить все задачи
```http
GET /tasks/
Authorization: Bearer {access_token}
```

#### Получить задачу по ID
```http
GET /tasks/{id}
Authorization: Bearer {access_token}
```

#### Создать новую задачу
```http
POST /tasks/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "string",
  "text": "string",
  "state": "string"
}
```

**Пример ответа:**
```json
{
  "name": "string",
  "text": "string",
  "state": "string",
  "id": 40,
  "date": "2026-02-16T09:30:30.570438+03:00",
  "user_id": 53
}
```

#### Обновить задачу
```http
PUT /tasks/{id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "string",
  "text": "string",
  "state": "string"
}
```

#### Удалить задачу
```http
DELETE /tasks/{id}
Authorization: Bearer {access_token}
```

## 🗄️ Управление миграциями базы данных

Миграции применяются автоматически при запуске контейнера (выполняется `alembic upgrade head`).  
Для ручного управления можно зайти в контейнер:
Миграции применяются автоматически при запуске контейнера (выполняется `alembic upgrade head`).  
Для ручного управления можно зайти в контейнер:
```bash
docker exec -it tasks-api-api-1 bash   # имя контейнера может отличаться
alembic current
alembic upgrade head
docker exec -it tasks-api-api-1 bash   # имя контейнера может отличаться
alembic current
alembic upgrade head
```

## 🏗️ Архитектура

### Слоистая архитектура
1. **API Layer** (`api/routes/`) - Маршруты FastAPI
2. **Service Layer** (`services/`) - Бизнес-логика
3. **Repository Layer** (`repositories/`) - Работа с базой данных через SQLAlchemy
4. **Database Layer** (`database/`) - Модели SQLAlchemy и управление соединением
5. **Models Layer** (`models/`) - Pydantic модели для API
6. **Utils Layer** (`utils/`) - Вспомогательные функции

### Аутентификация
- JWT токены с временем жизни
- Хеширование паролей с использованием Passlib
- Bearer аутентификация для защищенных эндпоинтов

### База данных (SQLAlchemy + Alembic)
- **SQLAlchemy ORM**: Современный доступ к данным через объекты
- **Alembic миграции**: Управление изменениями схемы базы данных
- **Асинхронная поддержка**: Готова к переходу на async/await
- **Сессии**: Управление транзакциями через сессии SQLAlchemy

### Логирование
- Раздельные логи для разных модулей
- Ротация логов по дням
- Настройка уровня логирования через переменные окружения

### Особенности тестирования:
- **Изоляция БД**: Использование временной БД для тестов
- **Моки и стабы**: Тестирование без внешних зависимостей
- **Интеграционные тесты**: Проверка полного цикла запросов
- **Тестирование SQLAlchemy**: Проверка репозиториев и моделей

---

⭐ Если вам понравился этот проект, не забудьте поставить звезду на GitHub!