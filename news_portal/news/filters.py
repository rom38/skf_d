from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput

from .models import Post


class PostFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='time_create',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local', 'class': 'form-control'},
        ),
    )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        fields = {
            # поиск по названию
            'head': ['icontains'],
            'post_type': ['exact'],
            'category': ['exact'],
        }
