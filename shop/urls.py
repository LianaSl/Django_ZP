from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    HomeView, ProductsListView, login_view, AboutUsView, hello,
    ProductDetailView, ProductCreateView, ProductUpdateView,
    ProductDeleteView, RegisterView, contacts_page, add_cart, CartTemplateView,
    cart_increase, cart_decrease, cart_remove, cart_clear,
    checkout, order_success,
)


urlpatterns = [
    path('', HomeView.as_view(), name='home_page'),
    path('products/', ProductsListView.as_view(), name='products_page'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
    path('about/', AboutUsView.as_view(), name='about_us_page'),
    path('hello/<str:name>/', hello, name='hello_page'),
    path('product/create/', ProductCreateView.as_view(), name='create_product'),
    path('product/update/<int:id>/', ProductUpdateView.as_view(), name='update_product'),
    path('product/delete/<int:id>/', ProductDeleteView.as_view(), name='product_delete'),
    path('login/', login_view, name='login'),
    path('contacts/', contacts_page, name='contacts_page'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('add_cart/<int:id>/', add_cart, name='cart_product'),
    path('cart/', CartTemplateView.as_view(), name='cart'),
    path('register/', RegisterView.as_view(), name='register'),
    path('cart/increase/<int:id>/', cart_increase, name='cart_increase'),
    path('cart/decrease/<int:id>/', cart_decrease, name='cart_decrease'),
    path('cart/remove/<int:id>/', cart_remove, name='cart_remove'),
    path('cart/clear/', cart_clear, name='cart_clear'),
    path('checkout/', checkout, name='checkout'),
    path('order/<int:id>/done/', order_success, name='order_success'),
]