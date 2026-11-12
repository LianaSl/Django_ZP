from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Název')
    description = models.TextField(blank=True, verbose_name='Popis')

    class Meta:
        verbose_name = 'Kategorie'
        verbose_name_plural = 'Kategorie'
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractUser):
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('10000.00'),
        verbose_name='Zůstatek',
    )

    class Meta:
        verbose_name = 'Uživatel'
        verbose_name_plural = 'Uživatelé'

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Název')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Cena',
        validators=[MinValueValidator(Decimal('0.01'), message='Cena musí být větší než 0.')],
        error_messages={
            'invalid': 'Zadejte platné číslo, například 199.90.',
            'max_digits': 'Cena má příliš mnoho číslic.',
            'max_whole_digits': 'Cena je příliš vysoká.',
            'max_decimal_places': 'Cena může mít nejvýše 2 desetinná místa.',
        },
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name='Množství')
    description = models.TextField(blank=True, verbose_name='Popis')
    is_stock = models.BooleanField(default=True, verbose_name='Skladem')
    image = models.ImageField(
        upload_to='shop/products/',
        blank=True,
        null=True,
        verbose_name='Obrázek',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'webp'])],
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Kategorie',
    )

    class Meta:
        verbose_name = 'Produkt'
        verbose_name_plural = 'Produkty'

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Nová'),
        ('paid', 'Zaplacená'),
        ('shipped', 'Odeslaná'),
        ('cancelled', 'Zrušená'),
    ]
    PAYMENT_CHOICES = [
        ('balance', 'Z účtu (zůstatek)'),
        ('transfer', 'Bankovní převod'),
        ('cod', 'Dobírka'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='Uživatel',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Vytvořeno')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Stav'
    )
    full_name = models.CharField(max_length=150, verbose_name='Jméno a příjmení')
    phone = models.CharField(max_length=30, verbose_name='Telefon')
    address = models.CharField(max_length=255, verbose_name='Adresa')
    city = models.CharField(max_length=100, verbose_name='Město')
    zip_code = models.CharField(max_length=10, verbose_name='PSČ')
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_CHOICES, verbose_name='Způsob platby'
    )
    shipping_price = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, verbose_name='Doprava'
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Celkem')

    class Meta:
        verbose_name = 'Objednávka'
        verbose_name_plural = 'Objednávky'
        ordering = ['-created_at']

    def __str__(self):
        return f'Objednávka #{self.pk} ({self.user})'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items', verbose_name='Objednávka'
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Produkt')
    # název a cena v okamžiku objednávky
    product_name = models.CharField(max_length=200, verbose_name='Název produktu')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cena')
    quantity = models.PositiveIntegerField(verbose_name='Množství')

    class Meta:
        verbose_name = 'Položka objednávky'
        verbose_name_plural = 'Položky objednávky'

    def __str__(self):
        return f'{self.product_name} × {self.quantity}'