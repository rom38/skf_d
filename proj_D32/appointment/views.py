from datetime import datetime

from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import send_mail

from .models import Appointment


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # отправляем письмо
        send_mail(
            # имя клиента и дата записи будут в теме для удобства
            subject=(
                f'{appointment.client_name}'
                f'{appointment.date.strftime("%Y-%M-%d")}'),
            # сообщение с кратким описанием проблемы
            message=appointment.message,
            # здесь указываете почту, с которой будете
            # отправлять (об этом попозже)
            from_email='peterbadson@yandex.ru',
            # здесь список получателей. Например,
            # секретарь, сам врач и т. д.
            recipient_list=[]
        )

        return redirect('appointments:make_appointment')
