from rest_framework import serializers
from books.models import Book, Genre, Author



class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['title']

class AuthorSerializer(serializers.ModelSerializer):
    book_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Author
        fields = ['title', 'book_count']

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    genre = GenreSerializer()

    class Meta:
        model = Book
        fields = ['id', 'title', 'image', 'authors', 'genre', 'count']
