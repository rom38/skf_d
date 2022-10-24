from django.urls import path
# Импортируем созданное нами представление
from .views import (
   NewsList, NewsDetail, NewsSearch,
   PostCreate, PostUpdate, PostDelete, CategoryNewsList)


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', NewsList.as_view(), name='news_list'),
   path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
   path('search/', NewsSearch.as_view()),
   path('create/', PostCreate.as_view(), name='news_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='news_create'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('categories/<int:pk>', CategoryNewsList.as_view(), name='categories'),
]
