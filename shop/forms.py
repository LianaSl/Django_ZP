from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Category, Product
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Product, Order



class MessageForm(forms.Form):
    message = forms.CharField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 5:
            raise ValidationError("User_name must be at least 5 characters long.")
        return username


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Uživatelské jméno'
        self.fields['password1'].label = 'Heslo'
        self.fields['password2'].label = 'Potvrzení hesla'

        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = 'Minimálně 8 znaků'
        self.fields['password2'].help_text = ''


class LoginForm(forms.Form):
    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("user_name")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError("Invalid username or password.")
            self.user = user
        return cleaned_data

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "phone", "address", "city", "zip_code", "payment_method"]
        labels = {
            "full_name": "Jméno a příjmení",
            "phone": "Telefon",
            "address": "Ulice a číslo domu",
            "city": "Město",
            "zip_code": "PSČ",
            "payment_method": "Způsob platby",
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Jana Nováková"}),
            "phone": forms.TextInput(attrs={"placeholder": "+420 123 456 789"}),
            "address": forms.TextInput(attrs={"placeholder": "Hlavní 12"}),
            "city": forms.TextInput(attrs={"placeholder": "Praha"}),
            "zip_code": forms.TextInput(attrs={"placeholder": "160 00"}),
        }