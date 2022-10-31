from django.db.models.signals import m2m_changed
# импортируем нужный декоратор
from django.dispatch import receiver
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
from .models import PostCategory
# from news_portal.settings import SITE_URL, DEFAULT_FROM_EMAIL
from .tasks import send_notify


# def send_notify(preview, pk, head, subscribers):
#     html_content = render_to_string(
#         'news_notify.html', {
#             'text': preview,
#             'head': head,
#             'link': f'{SITE_URL}/news/{pk}'
#         }
#     )
#     msg = EmailMultiAlternatives(
#         subject=head,
#         body='',
#         from_email=DEFAULT_FROM_EMAIL,
#         to=subscribers,
#     )
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()
        subscribers = [ittem.email for ittem in subscribers]
        send_notify.delay(instance.preview(),
                    instance.pk, instance.head, subscribers)
