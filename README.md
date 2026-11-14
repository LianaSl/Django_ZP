# Django_ZP
# LianaShop – internetový obchod „FLORENTINA“

Studijní internetový obchod s parfémy a kosmetikou vytvořený v Djangu. Zákazník si prohlíží katalog, přidává zboží do košíku a objednává. Administrátor spravuje produkty a objednávky.

## Funkce

- Hlavní stránka a stránka s kontakty.
- Registrace, přihlášení a odhlášení (vlastní uživatelský model `shop.User` se zůstatkem na účtu).
- Katalog produktů s fotografií, názvem a cenou, řazení podle ceny.
- Detail produktu s popisem, cenou a počtem kusů skladem.
- Košík uložený v session. Při přidání zboží se kontroluje skladová zásoba a zobrazí se potvrzující zpráva.
- Objednávka (pro přihlášené): doručovací údaje, platba ze zůstatku, bankovním převodem nebo dobírkou. Doprava zdarma od 1 500 Kč.
- Stránka „Objednávka přijata“.
- Pro administrátora (superuser): přidávání, úprava a mazání produktů, přehled objednávek v administraci.
- Kontrola zadané ceny s jasnou chybovou zprávou u pole.
- Uživatelské rozhraní v češtině.

## Technologie

- Python 3.12+, Django 6.1
- PostgreSQL
- HTML, CSS (bez frameworků)
- Django session pro košík

## Stránky

| Adresa | Co se otevře |
|---|---|
| `/shop/` | Hlavní stránka |
| `/shop/products/` | Katalog |
| `/shop/products/<id>/` | Detail produktu |
| `/shop/cart/` | Košík a objednávka |
| `/shop/order/<id>/done/` | Objednávka přijata |
| `/shop/login/` | Přihlášení |
| `/shop/register/` | Registrace |
| `/shop/contacts/` | Kontakt |
| `/shop/product/create/` | Přidání produktu (administrátor) |
| `/admin/` | Administrace |

## Spuštění

1. Vytvořte a aktivujte virtuální prostředí:

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

2. Nainstalujte závislosti:

   ```
   pip install -r requirements.txt
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

## Testy

```
python manage.py test
```

Testy ověřují registraci (vlastní uživatelský model), kontrolu ceny s různými hodnotami, přidání do košíku a objednávku se zůstatkem. Při spuštění testů se používá SQLite (viz konec `config/settings.py`), takže nejsou potřeba práva k vytvoření databáze v PostgreSQL.

## Struktura projektu

```
config/             nastavení projektu (settings.py, urls.py)
shop/               hlavní aplikace
  models.py         modely (User, Category, Product, Order, OrderItem)
  views.py          views
  forms.py          formuláře
  mixins.py         přístup pouze pro administrátora
  urls.py           adresy aplikace
  admin.py          administrace
  tests.py          automatické testy
  templates/shop/   HTML šablony
  static/shop/      styly (css), obrázky (images), skripty (js)
templates/          společná šablona base.html a nav.html
media/              nahrané fotografie produktů
```

## Autor

Liana Šljonkina
