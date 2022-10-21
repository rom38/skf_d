from datetime import datetime

from django.db import models


class Appointment(models.Model):
    date = models.DateField(
        default=datetime.utcnow,
    )
    client_name = models.CharField(
        max_length=200
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.client_name}: {self.message}'
