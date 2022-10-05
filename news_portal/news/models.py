from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Author(models.Model):
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating_q = self.post_set.aggregate(post_r=models.Sum('rating'))
        post_rating = 0
        post_rating += post_rating_q.get('post_r')

        comm_rating_q = self.auth_user.comment_set.aggregate(comm_r=models.Sum('rating'))
        comm_rating = 0
        comm_rating += comm_rating_q.get('comm_r')

        comm_auth_rating_q = Comment.objects.filter(post__author=self).aggregate(comm_auth_r=models.Sum('rating'))
        comm_auth_rating = 0
        comm_auth_rating += comm_auth_rating_q.get('comm_auth_r')

        self.auth_rating = post_rating*3+comm_rating+comm_auth_rating
        self.save()

    def __str__(self):
        return f'Author: {self.auth_user.username}'

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return str(self.name)


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
    text = models.TextField(default='')
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) > 124:
            return f"{self.text[:125]}..."
        return f"{self.text}"

    def __str__(self):
        return f'{self.post_type} {self.head}'


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.post.head} - {self.category.name}'

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text[:20]}...'
