from turtle import position
from django.db import models

# Create your models here.

class Order(models.Model):
    pass


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)


class Stuff(models.Model):
    director = 'DI'
    admin = 'AD'
    cook = 'CO'
    cashier = 'CA'
    cleaner = 'CL'

    POSITIONS = [
        (director, 'Директор'),
        (admin, 'Администратор'),
        (cook, 'Повар'),
        (cashier, 'Кассир'),
        (cleaner, 'Уборщик')
    ]
    full_name = models.CharField(max_length=64)
    position = models.CharField(max_length=2, choices=POSITIONS, default=cashier)
    labor_contract = models.IntegerField()


class ProductOrder(models.Model):
    pass
