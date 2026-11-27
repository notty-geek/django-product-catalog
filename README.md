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

### Make shortcuts

On macOS or Linux with GNU Make, run the following from the repository root for a fresh checkout. The targets use the project's virtual environment directly.

```sh
make setup
export DJANGO_SECRET_KEY="$(.venv/bin/python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
make migrate
make load-sample
make createsuperuser
make run
```

Run `make help` for the full list, `make verify` for system checks, migration drift, and tests, or `make run PORT=8001` to use another port. `make dump-sample` writes catalog fixture JSON to standard output.

Sign in with the superuser account you just created at [Django admin](http://127.0.0.1:8000/admin/). Migrations create `db.sqlite3` in the project root. Git ignores this local database, which also stores the admin account.

On a fresh database, `loaddata sample_catalog` loads 5 categories, 10 tags, and 20 products from the [sample fixture](catalog/fixtures/sample_catalog.json). For example, in admin, open **Products → Trail Coffee Flask** to see its Outdoors category and its Reusable, Insulated, and Stainless steel tags.

## Browser tests

With the virtual environment and `DJANGO_SECRET_KEY` set up as above, install the test dependencies and Playwright's headless Chromium once.

```sh
.venv/bin/python -m pip install -r requirements-e2e.txt
.venv/bin/python -m playwright install --only-shell chromium
make e2e
```

For subsequent runs, use `make e2e`. Django starts a live server on an available local port and loads the sample fixture into a disposable test database. Each scenario opens a fresh browser session and submits the catalog form. Run `make verify` for the separate Django checks and tests in [catalog/tests.py](catalog/tests.py).

I requested browser coverage of description matching, category selection, and the rule that every selected tag must match. I chose Playwright with Chromium. Codex wrote the [Behave scenarios](e2e/features/catalog_filters.feature), browser steps, test runner, and Make target.

## Catalog models

Each product requires a name, a description, and one category. Products can share a category and can have any number of tags, including zero. Category names are unique among categories, and tag names are unique among tags.

To delete a category in use, first reassign its products. Deleting a tag removes it from all associated products and preserves the products themselves.

## Search and filters

Open the [product catalog](http://127.0.0.1:8000/) to browse all products. The GET form accepts a description, one category, and any number of tags. Clear filters returns to the full catalog.

Search trims the input and matches it as one case-insensitive substring of the description. A product must match the selected category and **every** selected tag. Empty fields impose no restriction. For example, in the sample catalog, searching for `coffee` with the Outdoors category and the Insulated and Stainless steel tags returns only Trail Coffee Flask.

## AI attribution

OpenAI Codex ran Django's standard project and app generators, registered the empty catalog app, configured the signing key to come from the environment, added the dependency pin and Git ignore rules, and drafted this setup guide. The starter uses Django's generated SQLite and admin configuration.

OpenAI Codex wrote the development Makefile and documented its commands.

The applicant proposed one category per product and multiple tags per product, and approved the uniqueness and deletion rules. OpenAI Codex implemented the models and admin registration, ran Django's migration generator, and added tests for the relationship rules.

OpenAI Codex created the sample records through Django admin, exported them with Django's `dumpdata` command, and verified the fixture against the original catalog.

The applicant confirmed the description and tag matching rules. OpenAI Codex implemented the search form, view, template, filtering queryset, and request-level tests for those rules.

OpenAI Codex added the two product indexes approved by the applicant. The index on `name` supports alphabetical browsing, and the index on `(category, name)` supports alphabetical browsing within a category.
