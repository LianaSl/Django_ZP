from django.urls import path
from .views import home, products, about_us, hello, product_detail

urlpatterns = [
    path('', home, name='home_page'),
    path('products/', products, name='products_page'),
    path('products/<int:id>/', product_detail, name='product_detail'),
    path('about/', about_us, name='about_us_page'),
    path('hello/<str:name>/', hello, name='hello_page'),
    
    
]