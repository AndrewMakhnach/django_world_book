from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

class Genre(models.Model):
    name = models.CharField(max_length=20, help_text="choose a genre",
                            verbose_name="genres")
    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=20, help_text="choose a language",
                            verbose_name="language")
    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=30, help_text="author's name",
                                  verbose_name="author's first name")
    last_name = models.CharField(max_length=30, help_text="author's last name",
                                 verbose_name="author's last name")
    date_of_birth = models.DateField(help_text="date of birthday",
                                     verbose_name="date of birthday", null=True,
                                     blank=True)
    date_of_death = models.DateField(help_text="date of death",
                                     verbose_name="date of death", null=True,
                                     blank=True)
    def __str__(self):
        return self.last_name

class Book(models.Model):
    title = models.CharField(max_length=50, help_text="Book's title",
                             verbose_name="book's title")
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE,
                              help_text="choose a genre", verbose_name="genre",
                              null=True)
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 help_text="choose a language", null=True)
    author = models.ManyToManyField('Author', help_text="choose an author",
                                    verbose_name="author")
    summary = models.TextField(max_length=1000, help_text="short discription",
                               verbose_name="discription")
    isbn = models.CharField(max_length=13, help_text="13 symbols",
                            verbose_name="ISBN")

    def display_author(self):
        return ', '.join([author.last_name for author in self.author.all()])
    display_author.short_description = 'Authors'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

class Status(models.Model):
    name = models.CharField(max_length=20, help_text="status", verbose_name="status")

    def __str__(self):
        return self.name

class BookInstance(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    inv_nom = models.CharField(max_length=20, null=True,
                               help_text="inventory number",
                               verbose_name="inventory number")
    imprint = models.CharField(max_length=200, help_text="edition",
                              verbose_name="edition")
    status = models.ForeignKey('Status', on_delete=models.CASCADE,
                               null=True, help_text="change status of instance",
                               verbose_name="status")
    due_back = models.DateField(null=True, blank=True, help_text="end term in this status",
                                verbose_name="Date of status end")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 verbose_name="Customer",
                                 help_text='Choose a customer')
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        return '%s %s %s' % (self.inv_nom, self.book, self.status)




















