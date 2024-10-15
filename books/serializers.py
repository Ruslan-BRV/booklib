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
        """Проверяет входные данные и создает/находит авторов и жанр, если они указаны."""
        request = self.context.get('request')

        if 'authors' in request.data:
            authors = self._get_or_create_authors(request.data['authors'])
            attrs['authors'] = authors

        if 'genre' in request.data:
            genre_title = request.data['genre'].get('title')
            if not genre_title:
                raise serializers.ValidationError('Поле title жанра обязательно.')
            attrs['genre'] = self._get_or_create_genre(genre_title)

        return attrs

    def _get_or_create_authors(self, authors_data):
        """Создает или получает авторов по переданным данным."""
        authors = []
        for author in authors_data:
            author_obj = Author.objects.get_or_create(title=author['title'])[0]
            authors.append(author_obj)
        return authors

    def _get_or_create_genre(self, genre_title):
        """Создает или получает жанр по переданному названию."""
        genre_obj = Genre.objects.get_or_create(title=genre_title)[0]
        return genre_obj

    def create(self, validated_data):
        """
        Создает новую запись книги.
        При необходимости, связывает её с авторами и жанром.
        """
        authors = validated_data.pop('authors', [])
        genre = validated_data.pop('genre', None)
        book = Book.objects.create(**validated_data)

        if authors:
            book.authors.set(authors)

        if genre:
            book.genre = genre
            book.save()

        return book

    def update(self, instance, validated_data):
        """
        Обновляет существующую запись книги.
        При необходимости, обновляет связи с авторами и жанром.
        """
        authors = validated_data.pop('authors', None)
        genre = validated_data.pop('genre', None)

        instance.title = validated_data.get('title', instance.title)
        instance.count = validated_data.get('count', instance.count)
        instance.image = validated_data.get('image', instance.image)

        if authors is not None:
            instance.authors.set(authors)

        if genre is not None:
            instance.genre = genre

        instance.save()
        return instance
