from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

# Create your views here.
from django.views.generic import (
            ListView, DetailView,
            CreateView, UpdateView, DeleteView, View)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache

from .models import Category, Post
from .filters import PostFilter
from .forms import PostForm


class NewsSearch(ListView):
    model = Post
    ordering = '-time_create'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    # Отфильтровываем из статей и новостей только новости
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['filterset'] = self.filterset
        return context


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
    paginate_by = 10

    # def get_queryset(self):
    #     return super().get_queryset().filter(post_type=Post.news)

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
    # model = Post
    template_name = 'neww.html'
    context_object_name = 'neww'
    queryset = Post.objects.all()

    # переопределяем метод получения объекта, как ни странно
    def get_object(self, *args, **kwargs):
        # кэш очень похож на словарь, и метод get действует так же.
        # Он забирает значение по ключу, если его нет, то забирает None.
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    permission_required = ('news.add_post',)
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'
    # raise_exception = True


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm
    permission_required = ('news.change_post',)
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


class CategoryNewsList(ListView):
    model = Post
    template_name = 'news_category.html'
    context_object_name = 'news_category'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        return (super().get_queryset().
                filter(category=self.category).
                order_by('-time_create'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


class Subscribe(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = request.user
        category = Category.objects.get(id=pk)
        category.subscribers.add(user)
        message = 'Вы успешно подписались на категорию'
        return render(request, 'news_subscribe.html', {'category': category,
                                                       'message': message})
