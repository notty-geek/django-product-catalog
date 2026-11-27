# Product catalog

A Django take-home project for searching product descriptions and filtering products by category and tags. You can manage products, categories, and tags in Django admin using a local SQLite database.

## Run locally

Tested with Python 3.14.5 and Django 5.2.19. From the directory containing `manage.py`, run the following on macOS or Linux.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export DJANGO_SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
python manage.py migrate
python manage.py loaddata sample_catalog
python manage.py createsuperuser
python manage.py runserver
```

The export sets a random signing key for the current shell. When opening a new shell, activate the virtual environment and set `DJANGO_SECRET_KEY` again. Reuse the same value from your private environment settings to keep existing admin sessions valid across restarts.

Sign in with the superuser account you just created at [Django admin](http://127.0.0.1:8000/admin/). Migrations create `db.sqlite3` in the project root. Git ignores this local database, which also stores the admin account.

On a fresh database, `loaddata sample_catalog` loads 5 categories, 10 tags, and 20 products from the [sample fixture](catalog/fixtures/sample_catalog.json). For example, in admin, open **Products → Trail Coffee Flask** to see its Outdoors category and its Reusable, Insulated, and Stainless steel tags.

## Catalog models

Each product requires a name, a description, and one category. Products can share a category and can have any number of tags, including zero. Category names are unique among categories, and tag names are unique among tags.

To delete a category in use, first reassign its products. Deleting a tag removes it from all associated products and preserves the products themselves.

## Search and filters

Open the [product catalog](http://127.0.0.1:8000/) to browse all products. The GET form accepts a description, one category, and any number of tags. Clear filters returns to the full catalog.

The filtering queryset is the remaining implementation step. Until it is connected, submitting a filter displays a pending message. The agreed behavior is to trim the search text and match it as one case-insensitive substring of the description. A product must match the selected category and **every** selected tag. Empty fields impose no restriction. For example, in the sample catalog, searching for `coffee` with the Outdoors category and the Insulated and Stainless steel tags should return only Trail Coffee Flask.

## AI attribution

OpenAI Codex ran Django's standard project and app generators, registered the empty catalog app, configured the signing key to come from the environment, added the dependency pin and Git ignore rules, and drafted this setup guide. The starter uses Django's generated SQLite and admin configuration.

The applicant proposed one category per product and multiple tags per product, and approved the uniqueness and deletion rules. OpenAI Codex implemented the models and admin registration, ran Django's migration generator, and added tests for the relationship rules.

OpenAI Codex created the sample records through Django admin, exported them with Django's `dumpdata` command, and verified the fixture against the original catalog.

OpenAI Codex implemented the search form, page view, template, and tests for passing validated inputs to the applicant's queryset integration point.
