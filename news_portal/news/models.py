from operator import mod
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):

    article = 'AR'
    news = 'NW'

    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POSITIONS, default=news)
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField('Category',
               through='Postcategory')
    head = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField()


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete = models.CASCADE)
    category = models.ForeignKey('Category', on_delete = models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

