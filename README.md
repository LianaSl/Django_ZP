# Django_ZP
# LianaShop – internetový obchod „FLORENTINA“

Studijní internetový obchod s parfémy a kosmetikou vytvořený v Djangu. Zákazník si prohlíží katalog a přidává zboží do košíku, administrátor spravuje produkty přímo na webu.

## Funkce

- Hlavní stránka a stránka s kontakty.
- Registrace, přihlášení a odhlášení (vlastní uživatelský model `shop.User`).
- Katalog produktů s fotografií, názvem a cenou, řazení podle ceny. Katalog je dostupný jen po přihlášení.
- Detail produktu s popisem, cenou a počtem kusů skladem.
- Košík uložený v session. Při přidání zboží se kontroluje skladová zásoba.
- Pro administrátora (superuser): přidávání, úprava a mazání produktů.
- Uživatelské rozhraní v češtině.

## Technologie

- Python 3, Django 6.1
- PostgreSQL
- HTML, CSS (bez frameworků)
- Django session pro košík

## Stránky

| Adresa | Co se otevře |
|---|---|
| `/shop/` | Hlavní stránka |
| `/shop/products/` | Katalog (po přihlášení) |
| `/shop/products/<id>/` | Detail produktu |
| `/shop/cart/` | Košík |
| `/shop/login/` | Přihlášení |
| `/shop/register/` | Registrace |
| `/shop/contacts/` | Kontakt |
| `/shop/product/create/` | Přidání produktu (administrátor) |

## Spuštění

1. Vytvořte a aktivujte virtuální prostředí:

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

2. Nainstalujte závislosti (seznam je potřeba zkontrolovat podle projektu):

   ```
   pip install django psycopg2-binary pillow
   ```

3. Vytvořte databázi PostgreSQL a zadejte její údaje do souboru `config/settings.py`, do sekce `DATABASES`.

4. Spusťte migrace a vytvořte administrátora:

   ```
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. Spusťte server:

   ```
   python manage.py runserver
   ```

6. Otevřete v prohlížeči `http://127.0.0.1:8000/shop/`.

## Struktura projektu

```
config/        nastavení projektu (settings.py, urls.py)
shop/          hlavní aplikace
  models.py    modely (User, Product a další)
  views.py     views
  forms.py     formuláře
  mixins.py    přístup pouze pro administrátora
  urls.py      adresy aplikace
  templates/shop/   HTML šablony
static/shop/   styly (css), obrázky (images), skripty (js)
```

## Rozpracováno

- Stránka platby a dokončení objednávky.
- Stránka „Objednávka přijata“.

## Autor

Liana Šljonkina
