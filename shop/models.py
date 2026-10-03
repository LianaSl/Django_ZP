from django.db import models

from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('10000.00'),
        verbose_name='Баланс',
    )

    def __str__(self):
        return self.username

    class Products(models.Model):
        name = models.CharField(max_length=50)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        quantity = models.PositiveIntegerField()
        description = models.TextField()
        is_stock = models.BooleanField(default=True)
