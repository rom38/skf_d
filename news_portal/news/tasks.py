# import time
import datetime

from celery import shared_task

from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives
from news_portal.settings import SITE_URL, DEFAULT_FROM_EMAIL
from .models import Category, Post


@shared_task
def news_notify_weekly_task():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_create__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.
                      filter(name__in=categories).
                      filter(subscribers__email__isnull=False).
                      values_list('subscribers__email', flat=True))
    # subscribers
    print(subscribers)
    html_content = render_to_string(
        'news_notify_weekly.html', {
            # 'link': f'{SITE_URL}/news/{pk}',
            'link': SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Новости за неделю',
        body='Новости добавленные за неделю',
        from_email=DEFAULT_FROM_EMAIL,
        to=list(subscribers),
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    #  Your job processing logic here...
    print('hello from job')


@shared_task
def send_notify(preview, pk, head, subscribers):
    html_content = render_to_string(
        'news_notify.html', {
            'text': preview,
            'head': head,
            'link': f'{SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=head,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
