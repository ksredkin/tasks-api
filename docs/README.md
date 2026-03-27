# TasksAPI + Telegram Bot 🚀

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge\&logo=postgresql\&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge\&logo=sqlalchemy\&logoColor=white)
![Aiogram](https://img.shields.io/badge/Aiogram-2CA5E0?style=for-the-badge\&logo=telegram\&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge\&logo=jsonwebtokens\&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge\&logo=docker\&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-00A98F?style=for-the-badge\&logo=alembic\&logoColor=white)
![Unit Testing](https://img.shields.io/badge/Unit_Testing-4CAF50?style=for-the-badge)

---

## 📌 Описание

**TasksAPI** - это backend-сервис для управления задачами с Telegram-интерфейсом.

**Проект включает:**

* ⚡ **Backend API (FastAPI)** — REST API с JWT-аутентификацией
* 🤖 **Telegram Bot (Aiogram)** — удобный интерфейс для работы с задачами

Проект построен с упором на **чистую архитектуру**, масштабируемость и производительность.

---

## 🎯 Возможности

### 🔹 Backend (API)

* ✅ JWT-аутентификация (регистрация, логин)
* ✅ CRUD: задачи, папки (вложенные), пользователи
* ✅ Повторяющиеся задачи (daily / weekly / monthly)
* ✅ `due_date` и `visible_from`
* ✅ Статистика
* ✅ Alembic миграции
* ✅ Логирование
* ✅ Защита от брутфорса
* ✅ Покрытие тестами

### 🔹 Telegram Bot

* 🤖 Полный интерфейс управления задачами
* 🔐 Авторизация через API
* 📁 Вложенные папки
* 📝 Управление задачами
* 🔁 Повторения задач
* 📊 Статистика
* 💾 Импорт / экспорт данных
* ⏱️ Таймер

---

## 🚀 Запуск через Docker

### 1. Клонирование

```bash
git clone https://github.com/ksredkin/tasks-api.git
cd tasks-api
```

### 2. Настройка .env

```bash
cp .env.example .env
nano .env
```

### 3. Запуск

```bash
docker-compose up --build
```

---

## 🌐 Доступ

* API: http://localhost:8000
* Swagger: http://localhost:8000/docs
* Telegram Bot: через Telegram

---

Если проект оказался полезным — поставь ⭐ на GitHub!