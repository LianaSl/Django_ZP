from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Order, OrderItem, Product, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Zůstatek', {'fields': ('balance',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Zůstatek', {'fields': ('balance',)}),
    )
    list_display = UserAdmin.list_display + ('balance',)


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Product)
class AdminProducts(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'is_stock', 'category')
    search_fields = ('name',)
    list_filter = ('category',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'payment_method', 'total')
    list_filter = ('status', 'payment_method')
    search_fields = ('user__username', 'full_name')
    inlines = [OrderItemInline]