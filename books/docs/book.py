from books.serializers import BookSerializer
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