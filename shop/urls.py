from django.urls import path
from .views import HomeView, ProductsListView, login_view, AboutUsView, hello, product_detail, create_product, update_product, register, contacts_page

urlpatterns = [
    path('', HomeView.as_view(), name='home_page'),
    path('products/', ProductsListView.as_view(), name='products_page'),
    path('products/<int:id>/', product_detail, name='product_detail'),
    path('about/', AboutUsView.as_view(), name='about_us_page'),
    path('hello/<str:name>/', hello, name='hello_page'),
    path('product/create/', create_product, name='create_product'),
    path('product/update/<int:id>/', update_product, name='update_product'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('contacts/', contacts_page, name='contacts_page'),
]