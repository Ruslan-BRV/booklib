from django.db import models


    
class Genre(models.Model):
    title = models.CharField(max_length=100, db_column='Name', unique=True)

    class Meta:
        db_table = 'Genres'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.title}'



class Author(models.Model):
    title = models.CharField(max_length=100, db_column='Name', unique=True)

    class Meta:
        db_table = 'Authors'
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return f'{self.title}'
    
class Book(models.Model):
    title = models.CharField(max_length=255, db_column='Name', unique=True)
    image = models.ImageField(verbose_name="Изображение", upload_to="imageBooks/", default='default.jpg')
    authors = models.ManyToManyField('Author', related_name='books', verbose_name='Авторы')
    genre = models.ForeignKey(Genre, verbose_name="жанр", on_delete=models.CASCADE, related_name="genre", null=True) 
    count = models.IntegerField(verbose_name="Количество", default=0)

    class Meta:
        db_table = 'Books'
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return f'Книга {self.title}'
    