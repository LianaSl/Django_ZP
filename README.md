# LianaShop – online store "FLORENTINA"

A study online store with perfumes and cosmetics built with Django. Customers browse the catalogue, add items to the cart and place orders. The administrator manages products and orders.

## Features

- Home page and contact page.
- Registration, login and logout (custom user model `shop.User` with an account balance).
- Product catalogue with photo, name and price, sorted by price.
- Product detail with description, price and number of items in stock.
- Cart stored in the session. Stock availability is checked when an item is added, and a confirmation message is shown.
- Order (for logged-in users): delivery details, payment from account balance, bank transfer or cash on delivery. Free shipping from 1,500 CZK.
- "Order received" page.
- For the administrator (superuser): adding, editing and deleting products, overview of orders in the admin site.
- Price validation with a clear error message next to the field.
- User interface in Czech.

## Technologies

- Python 3.12+, Django 6.1
- PostgreSQL
- HTML, CSS (no frameworks)
- Django session for the cart

## Pages

| Address | What opens |
|---|---|
| `/shop/` | Home page |
| `/shop/products/` | Catalogue |
| `/shop/products/<id>/` | Product detail |
| `/shop/cart/` | Cart and checkout |
| `/shop/order/<id>/done/` | Order received |
| `/shop/login/` | Login |
| `/shop/register/` | Registration |
| `/shop/contacts/` | Contact |
| `/shop/product/create/` | Add product (administrator) |
| `/admin/` | Administration |

## Running the project

1. Create and activate a virtual environment:

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Create a PostgreSQL database and enter its credentials in `config/settings.py`, in the `DATABASES` section.

4. Run the migrations and create an administrator:

   ```
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. Start the server:

   ```
   python manage.py runserver
   ```

6. Open `http://127.0.0.1:8000/shop/` in your browser.

## Tests

```
python manage.py test
```

The tests cover registration (custom user model), price validation with various values, adding items to the cart and an order paid from the balance. SQLite is used when running the tests (see the end of `config/settings.py`), so no permission to create a database in PostgreSQL is needed.

## Project structure

```
config/             project settings (settings.py, urls.py)
shop/               main application
  models.py         models (User, Category, Product, Order, OrderItem)
  views.py          views
  forms.py          forms
  mixins.py         administrator-only access
  urls.py           application URLs
  admin.py          administration
  tests.py          automated tests
  templates/shop/   HTML templates
  static/shop/      styles (css), images, scripts (js)
templates/          shared templates base.html and includes/nav.html
media/              uploaded product photos
```

## Author

Liana Šljonkina
