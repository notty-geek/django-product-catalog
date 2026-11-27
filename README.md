# Product catalog

A Django take-home project for searching product descriptions and filtering products by category and tags. The starter includes an empty `catalog` app, a local SQLite database configuration, and Django admin.

## Run locally

Tested with Python 3.14.5 and Django 5.2.19. From the directory containing `manage.py`, run the following on macOS or Linux.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export DJANGO_SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The export sets a random signing key for the current shell. When opening a new shell, activate the virtual environment and set `DJANGO_SECRET_KEY` again. Reuse the same value from your private environment settings to keep existing admin sessions valid across restarts.

Sign in with the superuser account you just created at [Django admin](http://127.0.0.1:8000/admin/). Migrations create `db.sqlite3` in the project root. Git ignores this local database, which also stores the admin account.

## Finish the catalog

1. Define the product, category, and tag models in `catalog/models.py`. Run `python manage.py makemigrations catalog` and `python manage.py migrate`, then register the models in `catalog/admin.py`.
2. Use the admin interface to enter at least 5 categories, 10 tags, and 20 products. Once entered, document how a reviewer can load the same sample records in a fresh checkout.
3. Add a view, URL, and HTML form for description search and category and tag filters. Verify each filter individually and all three together.
4. Before submission, add the catalog page URL here and describe your relationship choices and how selecting multiple tags affects the results.

## AI attribution

OpenAI Codex ran Django's standard project and app generators, registered the empty catalog app, configured the signing key to come from the environment, added the dependency pin and Git ignore rules, and drafted this setup guide. The starter uses Django's generated SQLite and admin configuration.
