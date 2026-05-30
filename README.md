# EnglishWebsite

Веб-приложение для изучения и повторения английских слов.

---

## Стек

* Python
* Django
* PostgreSQL
* Docker / Docker Compose
* HTML / CSS / JS

---

## Функционал

* Регистрация и авторизация
* Создание собственных "колод" карточек с английскими словами
* Система изучения и повторения слов, отслеживание прогресса
* Библиотека из колод всех пользователей, поиск с фильтрами 
* Добавление чужих колод в избранное

---

## Запуск через Docker

### 1. Клонировать репозиторий

```bash
git clone https://github.com/your_username/EnglishWebsite.git
cd EnglishWebsite
```

### 2. Запустить проект

```bash
docker compose up --build
```

### 3. Применить миграции

```bash
docker compose exec web python manage.py migrate
```

### 4. Создать суперпользователя

```bash
docker compose exec web python manage.py createsuperuser
```

---

## Архитектура

Проект состоит из двух сервисов:

* **web** — Django backend
* **db** — PostgreSQL

Данные PostgreSQL сохраняются через Docker volume.
