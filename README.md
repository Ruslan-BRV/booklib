# Тестовый проект - бибилиотека книг "Booklib"

## Стек технологий
- `Django`
- `Django ORM`
- `Django Rest Framework`
- `Postgres`

## Описание проекта

Проект представляет собой API для библиотеки книг, позволяющий управлять информацией о книгах, авторах и жанрах. Он поддерживает основные операции CRUD (создание, чтение, обновление и удаление) и предоставляет статистические данные о книгах и авторах.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Ruslan-BRV/booklib.git

2. Перейдите в папку репозитория:
   ```bash
   cd booklib

3. Измените названия файла `.env.example` на `.env`

4. В файле `.env` введите свои настройки

5. В консоле введите:
    ```bash
    docker-compose up

6. Страница документации: http://127.0.0.1:8000/swagger/

## Эндпоинты

### Для книг:

1. **`GET /api/books`** — получение списка книг (с пагинацией).
2. **`GET /api/books/{book_id}`** — получение информации о конкретной книге.
3. **`POST /api/books`** — создание новой книги.
4. **`DELETE /api/books/{book_id}`** — удаление книги.
5. **`PUT /api/books/{book_id}`** — обновление информации о книге.
6. **`GET /api/books/copies?top=N`** - топ N книг по количеству экземпляров.

### Для авторов:

1. **`GET /api/authors`** — получение списка авторов (с пагинацией).
2. **`GET /api/authors/{author_id}`** — получение информации о конкретном авторе.
3. **`POST /api/authors`** — создание нового автора.
4. **`DELETE /api/authors/{author_id}`** — удаление автора.
5. **`PUT /api/authors/{author_id}`** — обновление информации об авторе.
6. **`GET /api/authors/{author_id}/stat`** - количество книг у автора.
7. **`GET /api/authors/stat?page=N&page_count=M`** - количество книг по каждому автору.

## Модели

### Book (Книга)
- `id` — UUID (уникальный идентификатор)
- `title` — название книги
- `image` — изображение книги (опционально)
- `authors` — связь многие ко многим с моделью `Author`
- `genre` — связь один ко многим с моделью `Genre` (опционально)
- `count` — количество экземпляров

### Author (Автор)
- `id` — UUID (уникальный идентификатор)
- `title` — имя автора

### Genre (Жанр)
- `id` — UUID (уникальный идентификатор)
- `title` — название жанра

## Лицензия
Этот проект доступен под лицензией MIT. Вы можете использовать, изменять и распространять этот проект в соответствии с условиями лицензии.
