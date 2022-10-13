from django_filters import FilterSet, DateFilter
from django.forms import DateTimeInput
from .models import Post


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    added_after = DateFilter(
        field_name='time_create',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%d',
            attrs={'type': 'date', 'class': 'form-control'},
        ),
    )
    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'head': ['icontains'],
            # количество товаров должно быть больше или равно
            'category': ['exact'],
            # 'time_create':['gt'],
        }
