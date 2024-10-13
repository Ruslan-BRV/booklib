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
        fields = ['id', 'title', 'book_count']

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(read_only=True, many=True)
    genre = GenreSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'image', 'authors', 'genre', 'count']

    def validate(self, attrs):
        request = self.context.get('request')
        if request.data.get('authors'):
            authors = []
            for author in request.data["authors"]:
                authors.append(
                    Author.objects.get_or_create(title=author["title"])[0]
                )
            attrs["authors"] = authors
        if request.data.get('title'):
            if not request.data['genre'].get('title'):
                raise serializers.ValidationError({'genre': 'Поле title жанра обязательно'})
            attrs['genre'] = Genre.objects.get_or_create(title=request.data['genre']['title'])[0]
        return attrs
