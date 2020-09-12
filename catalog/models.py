import uuid
from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Введите жанр книги.')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', null=True, on_delete=models.SET_NULL, related_name='books')
    summary = models.TextField(help_text='Описание книги')
    isbn = models.CharField('ISBN', max_length=13)
    genre = models.ManyToManyField(Genre, help_text='Выберите жанр для этой книги')

    def __str__(self):
        return self.title

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    date_of_death = models.DateField('Died', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    LOAN_STATUS = (('m', 'Maintenance'),
                   ('o', 'On load'),
                   ('a', 'Available'),
                   ('r', 'Reserved'))
    status = models.CharField(choices=LOAN_STATUS, max_length=1, blank=True, default='m', help_text='Доступность книг')

    class Meta:
        ordering = ['due_back']

    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
