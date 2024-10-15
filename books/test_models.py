import pytest

from django.db import transaction

from books.models import Author, Genre, Book

@pytest.mark.django_db
class TestModels:

    def test_genre_creation(self):
        genre = Genre.objects.create(title="Фантастика")
        assert genre.title == "Фантастика"
        assert str(genre) == "Фантастика"

    def test_author_creation(self):
        author = Author.objects.create(title="Лев Толстой")
        assert author.title == "Лев Толстой"
        assert str(author) == "Лев Толстой"

    def test_book_creation(self):
        genre = Genre.objects.create(title="Фантастика")
        author = Author.objects.create(title="Лев Толстой")
        book = Book.objects.create(
            title="Война и мир",
            image='imageBooks/default.jpg',
            genre=genre,
            count=5
        )
        book.authors.add(author)

        assert book.title == "Война и мир"
        assert book.count == 5
        assert book.genre == genre
        assert author in book.authors.all()
        assert str(book) == "Книга Война и мир"

    def test_unique_genre_constraints(self):
        Genre.objects.create(title="Детектив")
        with pytest.raises(Exception):
            Genre.objects.create(title="Детектив")  # Должно вызвать исключение

    def test_unique_author_constraints(self):
        Author.objects.create(title="Федор Достоевский")
        with pytest.raises(Exception):
            Author.objects.create(title="Федор Достоевский")  # Должно вызвать исключение

    def test_unique_book_constraints(self):
        genre = Genre.objects.create(title="Роман")
        Book.objects.create(
            title="Преступление и наказание",
            image='imageBooks/default.jpg',
            genre=genre,
            count=3
        )
        with pytest.raises(Exception):
            Book.objects.create(
                title="Преступление и наказание",
                image='imageBooks/default.jpg',
                genre=genre,
                count=2
            )  # Должно вызвать исключение
