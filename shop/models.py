from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractUser):
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('10000.00'),
        verbose_name='Баланс',
    )

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    is_stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to='shop/products/',
          blank=True,
            null=True,
            validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif','webp'])]
            )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()

        if self.price < 0:
            raise ValidationError({'price': 'Цена не может быть отрицательной.'})