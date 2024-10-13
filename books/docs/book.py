from books.models import Book
from books.serializers import AuthorSerializer, BookSerializer, GenreSerializer
from drf_yasg import openapi
from rest_framework import status



BOOK_DOCS = {
    'operation_id': "Список книг",
    "operation_description": "Выводит список всех книг",
    'manual_parameters': [
        openapi.Parameter(
            'title', openapi.IN_QUERY,
            description="Заголовок для поиска",
            type=openapi.TYPE_STRING,
            required=False,
            default=""
        ),
    ],
    'responses': {
        status.HTTP_200_OK: BookSerializer(many=True),
    },
}

GENRE_DOCS = {
    'operation_id': "Список жанров",
    "operation_description": "Выводит список всех жанров",
    'responses': {
        status.HTTP_200_OK: GenreSerializer(many=True),
    },
}

AUTHOR_DOCS = {
    'operation_id': "Список авторов",
    "operation_description": "Выводит список всех авторов",
    'responses': {
        status.HTTP_200_OK: AuthorSerializer(many=True),
    },
}

BOOK_TOP_DOCS = {
    'operation_id': "Список топ книг по количеству",
    "operation_description": "Выводит топ книг по количеству",
    'manual_parameters': [
        openapi.Parameter(
            'top', openapi.IN_QUERY,
            description="Количество книг в топе",
            type=openapi.TYPE_STRING,
            required=False,
            default=""
        ),
    ],
    'responses': {
        status.HTTP_200_OK: BookSerializer(many=True),
    },
}

BOOK_DELIVERY_DOCS = {
    'operation_id': "Загрузка книг",
    "operation_description": "Загрузка книг из JSON файла",
    'responses': {
        status.HTTP_200_OK: BookSerializer(many=True),
    },
}

BOOK_DETAIL_DOCS = {
    'operation_id': "Книга по id",
    'operation_description': "Получение книги по id",
    'responses': {
        200: openapi.Response('Информация о книге', BookSerializer),
        404: openapi.Response('Книга не найдена'),
    },
}

GENRE_DETAIL_DOCS = {
    'operation_id': "Жанр по id",
    'operation_description': "Получение жанра по id",
    'responses': {
        200: openapi.Response('Информация о жанре', GenreSerializer),
        404: openapi.Response('Жанр не найден'),
    },
}

AUTHOR_DETAIL_DOCS = {
    'operation_id': "Автор по id",
    'operation_description': "Получение автора по id",
    'responses': {
        200: openapi.Response('Информация об авторе', AuthorSerializer),
        404: openapi.Response('Автор не найден'),
    },
}