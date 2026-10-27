from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from shop.models import Product
from .forms import MessageForm, CategoryForm, ProductCreateForm, RegisterForm, LoginForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django. views import View
from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect


class HomeView(View):
    http_method_names =["get"]

    def get(self, request, *args, **kwargs):
        context = {
                "name": "John Doe",
                "age": 30,
                "list" : [1,2,3,4,5],
                "tuple" : (1,2,3,4,5),
                "set" : {1,2,3,4,5},
                "dict" : {"city": "Prague"}
           
    }
        return render(request, "shop/home.html", context)

class AboutUsView(View):
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        form = CategoryForm()
        return render(request, "shop/about_us.html", {"form": form})
        
    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            form = CategoryForm()
        return render(request, "shop/about_us.html", {"form": form})

  
products_list = [
        {
        "id": 1,
        "title": "Ноутбук",
        "description": "Универсальный ноутбук для работы, учебы и повседневных задач. Подходит для работы с документами, просмотра фильмов, общения в интернете и запуска большинства офисных приложений.",
        "price": 25000,
        "quantity": 5
    },
    {
        "id": 2,
        "title": "Смартфон",
        "description": "Современный смартфон с большим экраном, хорошей камерой и производительным процессором. Подходит для социальных сетей, фотографий, просмотра видео, игр и повседневного использования.",
        "price": 15000,
        "quantity": 12
    },
    {
        "id": 3,
        "title": "Наушники",
        "description": "Беспроводные Bluetooth-наушники с качественным звуком и встроенным микрофоном. Удобны для прослушивания музыки, просмотра фильмов, онлайн-звонков и занятий спортом.",
        "price": 2500,
        "quantity": 20
    },
    {
        "id": 4,
        "title": "Клавиатура",
        "description": "Механическая клавиатура с удобными клавишами и быстрым откликом. Хорошо подходит для программирования, работы с текстом, повседневного использования и компьютерных игр.",
        "price": 1800,
        "quantity": 8
    },
    {
        "id": 5,
        "title": "Мышь",
        "description": "Беспроводная компьютерная мышь с эргономичной формой и точным сенсором. Подходит для работы за компьютером, учебы, просмотра сайтов и выполнения повседневных задач.",
        "price": 900,
        "quantity": 15
    },
    {
        "id": 6,
        "title": "Монитор",
        "description": "Монитор с диагональю 24 дюйма и разрешением Full HD. Обеспечивает четкое изображение и подходит для работы, программирования, просмотра фильмов и подключения к игровому компьютеру.",
        "price": 6500,
        "quantity": 4
    },
    {
        "id": 7,
        "title": "Веб-камера",
        "description": "Веб-камера с разрешением Full HD и встроенным микрофоном. Подходит для онлайн-занятий, видеоконференций, общения с друзьями и проведения рабочих встреч.",
        "price": 1200,
        "quantity": 7
    },
    {
        "id": 8,
        "title": "Колонки",
        "description": "Компактные компьютерные колонки с чистым и достаточно громким звуком. Подходят для прослушивания музыки, просмотра фильмов, игр и использования вместе с ноутбуком или компьютером.",
        "price": 1100,
        "quantity": 10
    },
    {
        "id": 9,
        "title": "Флешка",
        "description": "USB-флешка объемом 64 ГБ для хранения и переноса документов, фотографий, видео и других файлов. Компактный корпус позволяет удобно носить накопитель с собой.",
        "price": 450,
        "quantity": 30
    },
    {
        "id": 10,
        "title": "Power Bank",
        "description": "Портативный внешний аккумулятор емкостью 10000 mAh. Позволяет несколько раз зарядить смартфон и подходит для поездок, путешествий и ситуаций, когда рядом нет розетки.",
        "price": 1300,
        "quantity": 18
    },
    {
        "id": 11,
        "title": "USB-кабель",
        "description": "Прочный USB-кабель для зарядки мобильных устройств и передачи данных. Подходит для ежедневного использования дома, на работе или в автомобиле.",
        "price": 250,
        "quantity": 40
    },
    {
        "id": 12,
        "title": "Роутер",
        "description": "Беспроводной Wi-Fi роутер для организации домашней или небольшой офисной сети. Обеспечивает стабильное подключение смартфонов, ноутбуков, телевизоров и других устройств к интернету.",
        "price": 1900,
        "quantity": 6
    },
    {
        "id": 13,
        "title": "SSD накопитель",
        "description": "Быстрый твердотельный накопитель объемом 1 ТБ для хранения операционной системы, программ, игр и пользовательских файлов. Позволяет значительно ускорить загрузку компьютера и приложений.",
        "price": 3200,
        "quantity": 9
    },
    {
        "id": 14,
        "title": "Микрофон",


    }
]
# Create your views here.

class ProductsListView(ListView):
    template_name = "shop/products.html"
    model = Product
    context_object_name = "products"


# class ProductView(TemplateView):
#     template_name = "shop/products.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["products"] = Product.objects.all()
#         return context
        
    

def products(request):
    context = {
        "products": products_list
    }
    return render(request, "shop/products.html", context)

def about_us(request):
    if request.method == "GET":
        form = CategoryForm()
        return render(request, "shop/about_us.html", {"form": form})
       
    if request.method =="POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            form = CategoryForm()
    return render(request, "shop/about_us.html", {"form": form})
    


def hello(request, name):
    return HttpResponse(f"HELLO{name}")

def contacts_page(request):
    return render(request, 'shop/contacts_page.html')

def product_detail(request, id):
    context ={}
    try:
        prod = Product.objects.get(id=id)
        context["product"] = prod
    except Product.DoesNotExist:
        context["product"] = "Product not found"

    return render(request, "shop/product_detail.html", context)
          
def create_product(request):
    if request.method == "GET":
        form = ProductCreateForm()
        return render(request, "shop/create_product.html", {"form": form})
    if request.method == "POST":
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = ProductCreateForm()
        return render(request, "shop/create_product.html", {"form": form})

def update_product(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        redirect("products_page")
    if request.method == "POST":
       form = ProductCreateForm(request.POST, request.FILES, instance = product)
       if form.is_valid():
            form.save()
            return redirect(product_detail, id=product.id)
       return render(request, "shop/create_product.html", {"form": form})
    else:
        form = ProductCreateForm(instance=product)
        return render(request, "shop/create_product.html", {"form": form})   

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("products_page")
    else:
        form =RegisterForm()
    return render(request, "shop/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect("products_page")
    else:
         form = LoginForm()
    return render(request, "shop/login.html", {"form": form})  

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("products_page") 
    else:
        form = UserCreationForm()
    return render(request, "shop/register.html", {"form": form})