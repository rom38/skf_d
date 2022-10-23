from django.urls import path
# Импортируем созданное нами представление
from .views import (
    AppointmentView
)


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.

   path('make_appointment/', AppointmentView.as_view(), name='make_appointment'),

]
