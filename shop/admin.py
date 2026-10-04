from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Product, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Баланс', {'fields': ('balance',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Баланс', {'fields': ('balance',)}),
    )
    list_display = UserAdmin.list_display + ('balance',)


@admin.register(Product)
class AdminProducts(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'is_stock')
    search_fields = ('name', 'price'),
    list_filter = ('name', 'price') 