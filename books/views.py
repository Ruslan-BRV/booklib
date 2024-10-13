from books.models import Author, Book, Genre
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from books.serializers import AuthorSerializer, BookSerializer, GenreSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import models


# Класс пагинации с возможностью получения размера страницы через GET параметры
class Pagination(PageNumberPagination):
    page_size = 3

    def get_page_size(self, request):
        page_size = request.query_params.get('page_count')
        if page_size and page_size.isdigit():
            return int(page_size)
        return self.page_size


# ViewSet для модели Book
class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by('id')
    pagination_class = Pagination

    # Переопределение метода get_queryset для фильтрации книг по названию
    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(name__icontains=title)
        return queryset

    # Метод для получения списка топ-N книг
    def list_top_books(self, request):
        top_n = request.query_params.get('top', None)
        if top_n is not None:
            top_n = int(top_n)
            books = Book.objects.order_by('-count')[:top_n]
        else:
            books = Book.objects.all()

        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)


# ViewSet для модели Author
class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all().order_by('id')
    pagination_class = Pagination

    # Метод для получения количества книг автора
    @action(detail=True, methods=['get'])
    def stat(self, request, pk=None):
        author = self.get_object()
        book_count = author.books.count()
        return Response({'author': author.name, 'book_count': book_count})

    # Метод для получения статистики по всем авторам с возможностью пагинации, сортировка по количеству книг
    @action(detail=False, methods=['get'])
    def stats(self, request):
        authors = Author.objects.prefetch_related('books').annotate(
            book_count=models.Count('books')
        ).order_by('-book_count')
        page = self.paginate_queryset(authors)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(authors, many=True)
        return Response(serializer.data)


# ViewSet для модели Genre
class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all().order_by('id')
    pagination_class = Pagination


# Закомментированный пример класса для массовой доставки книг
# class BookDeliveryView(APIView):
#     def post(self, request):
#         books_data = request.data  # Ожидается массив объектов книг
#         for book_data in books_data:
#             title = book_data['title']
#             authors_data = book_data['authors']
#             count = book_data['count']
#
#             # Найдите или создайте авторов
#             authors = []
#             for author_data in authors_data:
#                 author, created = Author.objects.get_or_create(name=author_data['title'])
#                 authors.append(author)
#
#             # Найдите или создайте книгу
#             book, created = Book.objects.get_or_create(title=title)
#             book.quantity += count  # Увеличьте количество экземпляров
#             book.save()
#             book.authors.set(authors)  # Обновите связь с авторами
#
#         return Response(status=status.HTTP_201_CREATED)
