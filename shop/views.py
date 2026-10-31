from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from shop.models import Product
from .forms import CategoryForm, ProductCreateForm, LoginForm
from .mixins import AdminRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page  



class HomePageRedirect(RedirectView):
    url = reverse_lazy("home_page")


class HomeView(View):
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        color = request.COOKIES.get("my_color", "red")
        context = {
            "my_color": color
        }
        return render(request, "shop/home.html", context)

    def post(self, request, *args, **kwargs):
        color = request.POST.get("color")
        response = redirect(request.path)
        if color:
            response.set_cookie(
                key="my_color",
                value=color,
                httponly=True,
                samesite="Lax"
            )
        return response


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

@method_decorator(cache_page(90),name= "dispatch")
class ProductsListView(LoginRequiredMixin, ListView):
    template_name = "shop/products.html"
    model = Product
    context_object_name = "products"
    # paginate_by = 3
    ordering = ["price"]


def hello(request, name):
    return HttpResponse(f"HELLO{name}")


def contacts_page(request):
    return render(request, "shop/contacts_page.html")


class ProductDetailView(DetailView):
    template_name = "shop/product_detail.html"
    model = Product
    context_object_name = "product"
    pk_url_kwarg = "id"


class ProductCreateView(AdminRequiredMixin, CreateView):
    template_name = "shop/create_product.html"
    model = Product
    form_class = ProductCreateForm
    success_url = reverse_lazy("products_page")


class ProductUpdateView(AdminRequiredMixin, UpdateView):
    model = Product
    form_class = ProductCreateForm
    template_name = "shop/create_product.html"
    success_url = reverse_lazy("products_page")
    pk_url_kwarg = "id"


class ProductDeleteView(AdminRequiredMixin, DeleteView):
    model = Product
    pk_url_kwarg = "id"
    success_url = reverse_lazy("products_page")


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


def add_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart = request.session.get("cart", {})
    product_id = str(product.id)
    current_quantity = cart.get(product_id, 0)
    if current_quantity < product.quantity:
        cart[product_id] = current_quantity + 1
    request.session["cart"] = cart
    return redirect("products_page")


class CartTemplateView(TemplateView):
    template_name = "shop/cart_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get("cart", {})
        products = Product.objects.filter(id__in=cart.keys())
        context["products"] = products
        return context