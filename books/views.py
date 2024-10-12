from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic import DetailView
from books.models import Author, Book, Genre
from rest_framework import permissions, viewsets

from books.serializers import AuthorSerializer, BookSerializer, GenreSerializer



class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()



class BooksView(ListView):
    model = Book
    template_name = 'books/catalog.html'
    context_object_name = 'books'
    paginate_by = 30



class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

