from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.http import require_POST

from shop.models import Product, Order, OrderItem
from .forms import (
    CategoryForm, ProductCreateForm, LoginForm, RegisterForm, CheckoutForm,
)
from .mixins import AdminRequiredMixin

User = get_user_model()


# ---------------------------------------------------------------- pages

class HomePageRedirect(RedirectView):
    url = reverse_lazy("home_page")


class HomeView(View):
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        color = request.COOKIES.get("my_color", )
        context = {
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


def hello(request, name):
    return HttpResponse(f"HELLO{name}")


def contacts_page(request):
    return render(request, "shop/contacts_page.html")


# ---------------------------------------------------------------- products

class ProductsListView(ListView):
    template_name = "shop/products.html"
    model = Product
    context_object_name = "products"
    # paginate_by = 3
    ordering = ["price"]


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


# ---------------------------------------------------------------- login / register

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect("products_page")
    else:
        form = LoginForm()
    return render(request, "shop/login.html", {"form": form})


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "shop/register.html"
    success_url = reverse_lazy("products_page")


# ---------------------------------------------------------------- cart

FREE_SHIPPING_FROM = 1500   # free shipping from this amount (Kč)
SHIPPING_PRICE = 99         # shipping price (Kč)


def add_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart = request.session.get("cart", {})
    product_id = str(product.id)
    current_quantity = cart.get(product_id, 0)
    if current_quantity < product.quantity:
        cart[product_id] = current_quantity + 1
    request.session["cart"] = cart
    return redirect("products_page")


def get_cart_items(request):
    cart = request.session.get("cart", {})
    items, total = [], 0
    for p in Product.objects.filter(id__in=cart.keys()):
        qty = cart[str(p.id)]
        items.append({"product": p, "qty": qty, "sum": p.price * qty})
        total += p.price * qty
    return items, total


def cart_context(request, form=None):
    items, total = get_cart_items(request)
    shipping = 0 if (total >= FREE_SHIPPING_FROM or not items) else SHIPPING_PRICE
    return {
        "items": items,
        "total": total,
        "shipping": shipping,
        "grand_total": total + shipping,
        "free_from": FREE_SHIPPING_FROM,
        "form": form or CheckoutForm(),
    }


class CartTemplateView(TemplateView):
    template_name = "shop/cart_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(cart_context(self.request))
        return context


@require_POST
def cart_increase(request, id):
    product = get_object_or_404(Product, id=id)
    cart = request.session.get("cart", {})
    key = str(product.id)
    if cart.get(key, 0) < product.quantity:
        cart[key] = cart.get(key, 0) + 1
    request.session["cart"] = cart
    return redirect("cart")


@require_POST
def cart_decrease(request, id):
    cart = request.session.get("cart", {})
    key = str(id)
    if key in cart:
        cart[key] -= 1
        if cart[key] <= 0:
            del cart[key]
    request.session["cart"] = cart
    return redirect("cart")


@require_POST
def cart_remove(request, id):
    cart = request.session.get("cart", {})
    cart.pop(str(id), None)
    request.session["cart"] = cart
    return redirect("cart")


@require_POST
def cart_clear(request):
    request.session["cart"] = {}
    return redirect("cart")


# ---------------------------------------------------------------- order

class CheckoutError(Exception):
    pass


@login_required
@require_POST
def checkout(request):
    items, total = get_cart_items(request)
    if not items:
        return redirect("cart")

    form = CheckoutForm(request.POST)
    if not form.is_valid():
        return render(request, "shop/cart_page.html", cart_context(request, form))

    ctx = cart_context(request, form)
    shipping, grand_total = ctx["shipping"], ctx["grand_total"]

    try:
        with transaction.atomic():
            # lock products and check stock
            locked = {}
            for i in items:
                p = Product.objects.select_for_update().get(pk=i["product"].pk)
                if i["qty"] > p.quantity:
                    raise CheckoutError(
                        f"Nedostatek zboží: {p.name} (skladem {p.quantity} ks)."
                    )
                locked[p.pk] = p

            order = form.save(commit=False)
            order.user = request.user
            order.shipping_price = shipping
            order.total = grand_total

            # pay from balance
            if order.payment_method == "balance":
                user = User.objects.select_for_update().get(pk=request.user.pk)
                if user.balance < grand_total:
                    raise CheckoutError("Na účtu není dostatek prostředků.")
                user.balance -= grand_total
                user.save(update_fields=["balance"])
                order.status = "paid"

            order.save()
            for i in items:
                p = locked[i["product"].pk]
                OrderItem.objects.create(
                    order=order,
                    product=p,
                    product_name=p.name,
                    price=p.price,
                    quantity=i["qty"],
                )
                p.quantity -= i["qty"]
                p.save(update_fields=["quantity"])
    except CheckoutError as e:
        form.add_error(None, str(e))
        return render(request, "shop/cart_page.html", ctx)

    request.session["cart"] = {}
    return redirect("order_success", id=order.id)


@login_required
def order_success(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    return render(request, "shop/order_success.html", {"order": order})