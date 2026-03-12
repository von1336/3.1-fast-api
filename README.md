# Домашнее задание 3.1 — FastAPI ч.1

REST API объявлений купли/продажи на FastAPI (без авторизации).

Поля: заголовок, описание, цена, автор, дата создания.

- POST /advertisement — создание
- PATCH /advertisement/{id} — обновление
- DELETE /advertisement/{id} — удаление
- GET /advertisement/{id} — получение по id
- GET /advertisement?query_string — поиск по полям

Запуск: `uvicorn main:app --reload` или через Docker.
