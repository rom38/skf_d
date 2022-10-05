from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from .models import Post


class NewsList(ListView):
    model = Post
    ordering = '-time_create'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    # Отфильтровываем из статей и новостей только новости
    def get_queryset(self):
        return super().get_queryset().filter(post_type=Post.news)

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        # context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        # context['next_sale'] = None
        context['next_sale'] = "Распродажа в среду!"
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'neww.html'
    context_object_name = 'neww'
