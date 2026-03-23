# TasksAPI + Telegram Bot + Web Frontend 🚀

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Aiogram](https://img.shields.io/badge/Aiogram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-00A98F?style=for-the-badge&logo=alembic&logoColor=white)
![Unit Testing](https://img.shields.io/badge/Unit_Testing-4CAF50?style=for-the-badge&logo=testcafe&logoColor=white)

---

## 📌 Описание

**TasksAPI** - это fullstack-приложение для управления задачами, состоящее из:

- ⚡ **Backend API (FastAPI)** - REST API с JWT-аутентификацией  
- 🤖 **Telegram Bot (Aiogram)** - удобный интерфейс в Telegram  
- 🌐 **Web Frontend (React + Vite)** - веб-интерфейс (в разработке)

Проект построен с упором на **чистую архитектуру**, масштабируемость и разделение ответственности.

---

## 🎯 Возможности

### 🔹 Backend (API)
- ✅ JWT-аутентификация (регистрация, логин)
- ✅ CRUD: задачи, папки (вложенные), пользователи
- ✅ Повторяющиеся задачи (daily / weekly / monthly)
- ✅ `due_date` и `visible_from`
- ✅ Статистика по задачам
- ✅ Alembic миграции
- ✅ Логирование
- ✅ Rate limiting + защита от брутфорса
- ✅ Покрытие тестами

### 🔹 Telegram Bot
- 🤖 Полный интерфейс управления задачами
- 🔐 Авторизация через API
- 📁 Работа с папками (вложенность)
- 📝 Управление задачами
- 🔁 Повторения задач
- 📊 Статистика
- 🚀 Импорт задач
- ⏱️ Таймер
- 💾 Импорт и экспорт данных
- 🛡️ Защита от брутфорса

### 🔹 Web Frontend
- ⚛️ React + Vite
- ⚡ Быстрая сборка (Vite)
- 📦 Готов к интеграции с API
- 🚧 Пока в стадии разработки

---

## 📁 Структура проекта

```
.
├── bot/ # Telegram Bot (Aiogram)
├── tasks_api/ # Backend (FastAPI)
├── web-frontend/ # Frontend (React + Vite)
├── docker-compose.yml # Оркестрация
├── docs/ # Документация
└── logs/ # Логи
```

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

Заполни переменные.

### 3. Запуск
```bash
docker-compose up --build
```

### 🌐 Доступ
API: http://localhost:8080
Swagger: http://localhost:8080/docs
Frontend: http://localhost:8000
Telegram Bot: через Telegram

---

⭐ Если проект понравился — поставь звезду!