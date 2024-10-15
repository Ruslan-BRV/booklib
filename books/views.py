from functools import lru_cache

from django.db import models
from django.utils.decorators import method_decorator

from rest_framework import viewsets, serializers, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from books.models import Author, Book, Genre
from books.serializers import AuthorSerializer, BookSerializer, GenreSerializer
from books.docs.book import BOOK_DOCS, BOOK_TOP_DOCS, BOOK_DELIVERY_DOCS


class Pagination(PageNumberPagination):
    """Класс пагинации с возможностью получения размера страницы через GET параметры"""
    page_size = 3

    def get_page_size(self, request):
        page_size = request.query_params.get('page_count')
        if page_size and page_size.isdigit():
            return int(page_size)
        return self.page_size


@method_decorator(
    name='list', decorator=swagger_auto_schema(**BOOK_DOCS)
)
class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all().select_related('genre').prefetch_related('authors').order_by('id')
    pagination_class = Pagination

    def get_queryset(self):
        """Переопределение метода get_queryset для фильтрации книг по названию"""
        queryset = super().get_queryset()
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        return queryset

    @swagger_auto_schema(**BOOK_TOP_DOCS)
    def list_top_books(self, request):
        """Метод для получения списка топ-N книг"""
        top_n = request.query_params.get('top', None)
        if top_n is not None:
            top_n = int(top_n)
            books = Book.objects.order_by('-count')[:top_n]
        else:
            books = Book.objects.all()

        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all().prefetch_related('books').order_by('id')
    pagination_class = Pagination

    @action(detail=True, methods=['get'])
    def stat(self, request, pk=None):
        """Метод для получения количества книг автора"""
        author = self.get_object()
        book_count = author.books.count()
        return Response({'author': author.title, 'book_count': book_count})

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Метод для получения статистики по всем авторам с возможностью пагинации, 
        сортировка по количеству книг
        """
        authors = Author.objects.prefetch_related('books').annotate(
            book_count=models.Count('books')
        ).order_by('-book_count')
        page = self.paginate_queryset(authors)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(authors, many=True)
        return Response(serializer.data)


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all().order_by('id')
    pagination_class = Pagination


class BookDeliveryView(APIView):
    @swagger_auto_schema(**BOOK_DELIVERY_DOCS)
    def post(self, request):
        """Обрабатывает запрос на добавление или обновление книг.
        Если книга уже существует — увеличивает количество.
        Если книга повторяется в текущем запросе — обновляет её.
        Иначе — создаёт новую запись.
        """
        updated_books = []
        created_books = []
        for book in request.data:
            if not book['title']:
                 raise serializers.ValidationError("Название книги не может быть пустым.")
            title = book['title']
            count = book['count']
            #Ищем книгу в базе данных
            book_db = self._books.get(title)
            # Ищем книгу, которая была создана в текущем запросе, но повторяется еще раз
            created_book = list(filter(
                lambda x: x.title == title,
                created_books
            ))
            if book_db:
                 # Если книга существует, увеличиваем количество экземпляров
                book_db.count += count
                updated_books.append(book_db)
            elif created_book:
                # Если книга была создана в текущем запросе, обновляем количество
                created_book[0].count += count
                updated_books.append(created_book[0])
            else:
                if not book.get('authors'):
                    raise serializers.ValidationError("Поле авторы не может быть пустым.")
                authors_data = book['authors']
                # Добавляем либо создаем авторов
                authors = [
                    Author.objects.get_or_create(title=author_data['title'])[0]
                    for author_data in authors_data
                ]
                # Создаем новую книгу и добавляем её в базу
                book_db = Book.objects.create(
                    title=title,
                    count=count
                )
                book_db.authors.set(authors)
                if book.get('genre'):
                    if not book['genre'].get('title'):
                        raise serializers.ValidationError('Поле title жанра обязательно.')
                    book_db.genre = Genre.objects.get_or_create(title=book['genre']['title'])[0]
                    book_db.save()
                created_books.append(book_db)
        Book.objects.bulk_update(updated_books, ['count'])
        return Response(
            BookSerializer(Book.objects.all(), many=True).data,
            status=status.HTTP_201_CREATED
        )

    @property
    @lru_cache
    def _books(self):
        """Возвращает словарь всех книг из базы данных с их названиями в качестве ключей.
        Метод использует кэширование с помощью декоратора `lru_cache`, чтобы 
        сохранить результат первого вызова и использовать его повторно 
        для повышения производительности при последующих обращениях.
        """
        return {
            book.title: book
            for book in Book.objects.all()
        }     
