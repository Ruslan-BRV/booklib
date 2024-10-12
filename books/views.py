from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic import DetailView
from books.models import Author, Book, Genre


class BooksView(ListView):
    model = Book
    template_name = 'books/catalog.html'
    context_object_name = 'books'
    paginate_by = 30



class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

