from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import ProductCreateForm, RegisterForm
from .models import Category, Order, Product

User = get_user_model()

ORDER_DATA = {
    "full_name": "Jana Nováková",
    "phone": "+420123456789",
    "address": "Hlavní 12",
    "city": "Praha",
    "zip_code": "16000",
}


class RegistrationTest(TestCase):
    def test_form_uses_custom_user_model(self):
        self.assertIs(RegisterForm.Meta.model, User)

    def test_register_ok_and_duplicate_username(self):
        data = {"username": "lianka", "password1": "StrongPass12345",
                "password2": "StrongPass12345"}
        self.assertEqual(self.client.post(reverse("register"), data).status_code, 302)
        self.assertTrue(User.objects.filter(username="lianka").exists())

        response = self.client.post(reverse("register"), data)
        self.assertIn("username", response.context["form"].errors)


class PriceValidationTest(TestCase):
    def test_different_prices(self):
        category = Category.objects.create(name="Kosmetika")
        for price, valid in [("199.90", True), ("abc", False), ("0", False),
                             ("-5", False), ("12.345", False)]:
            form = ProductCreateForm(data={
                "name": "Rtěnka", "price": price, "quantity": 3,
                "is_stock": "on", "category": category.pk,
            })
            with self.subTest(price=price):
                self.assertEqual(form.is_valid(), valid)
                if not valid:
                    self.assertIn("price", form.errors)


class ShopFlowTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("kupujici", password="StrongPass12345")
        self.client.login(username="kupujici", password="StrongPass12345")
        category = Category.objects.create(name="Parfémy")
        self.product = Product.objects.create(
            name="Parfém", price=Decimal("500"), quantity=5, category=category
        )

    def test_add_to_cart_shows_message(self):
        url = reverse("cart_product", args=[self.product.id])
        response = self.client.post(url, follow=True)
        texts = [str(m) for m in response.context["messages"]]
        self.assertTrue(any("bylo přidáno do košíku" in t for t in texts))

    def test_order_paid_from_balance(self):
        self.client.post(reverse("cart_product", args=[self.product.id]))
        data = dict(ORDER_DATA, payment_method="balance")
        self.client.post(reverse("checkout"), data)

        order = Order.objects.get()
        self.assertEqual(order.status, "paid")
        self.user.refresh_from_db()
        self.product.refresh_from_db()
        self.assertEqual(self.user.balance, Decimal("9401.00"))  # 500 + 99 doprava
        self.assertEqual(self.product.quantity, 4)

    def test_order_not_enough_balance(self):
        self.user.balance = Decimal("100")
        self.user.save()
        self.client.post(reverse("cart_product", args=[self.product.id]))
        data = dict(ORDER_DATA, payment_method="balance")
        response = self.client.post(reverse("checkout"), data)

        self.assertContains(response, "Na účtu není dostatek prostředků.")
        self.assertEqual(Order.objects.count(), 0)
