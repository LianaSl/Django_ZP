from django.urls import path
from .views import (
    HomeView, ProductsListView, login_view, AboutUsView, hello,
    ProductDetailView, ProductCreateView, ProductUpdateView,
    ProductDeleteView, register, contacts_page, add_cart, CartTemplateView,
)
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', HomeView.as_view(), name='home_page'),
    path('products/', ProductsListView.as_view(), name='products_page'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
    path('about/', AboutUsView.as_view(), name='about_us_page'),
    path('hello/<str:name>/', hello, name='hello_page'),
    path('product/create/', ProductCreateView.as_view(), name='create_product'),
    path('product/update/<int:id>/', ProductUpdateView.as_view(), name='update_product'),
    path('product/delete/<int:id>/', ProductDeleteView.as_view(), name='product_delete'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('contacts/', contacts_page, name='contacts_page'),
    path('logout/', LogoutView.as_view(next_page='products_page'), name='logout'),
    path('add_cart/<int:id>/', add_cart, name='cart_product'),
    path('cart/', CartTemplateView.as_view(), name='cart'),
]