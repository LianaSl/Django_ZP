from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Order, OrderItem, Product, User

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Product)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'total')
    list_filter = ('status', 'payment_method')
    inlines = [OrderItemInline]