from books.models import Author, Book, Genre
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from books.serializers import AuthorSerializer, BookSerializer, GenreSerializer

class Pagination(PageNumberPagination):
    page_size = 3

class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by('id')
    pagination_class = Pagination

class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all().order_by('id')
    pagination_class = Pagination

class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all().order_by('id')
    pagination_class = Pagination
