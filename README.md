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

I made the catalog design decisions below and reviewed the resulting code, migrations, tests, sample data, and documentation. OpenAI Codex wrote the implementations listed here and ran the automated checks.

| Area | My proposal or decision | What Codex implemented and I reviewed |
| --- | --- | --- |
| Data model | I proposed one category per product and multiple tags per product. I approved protecting categories in use and allowing shared tags to be removed. | Product, Category, and Tag models, uniqueness rules, admin registration, generated migration, and relationship tests. |
| Search | I chose trimmed, case-insensitive substring matching on descriptions. Selecting two tags must narrow the list to products with both. The category and description restrictions still apply. | Search form, filtering queryset, view, template, and request-level tests for individual and combined filters. |
| Indexes | I requested indexing and approved the two indexes Codex proposed for alphabetical browsing across the catalog and within a category. | Indexes on `name` and `(category, name)` and their migration. |
| Sample catalog | I requested entry through Django admin and a fixture reviewers could load on a fresh checkout. | Entry of 5 categories, 10 tags, and 20 products through admin, fixture export with Django’s `dumpdata`, and verification against the original catalog. |
| Project setup and delivery | I chose SQLite, requested an environment-provided signing key and Make commands, and asked for a feature-branch and PR review workflow. | Django project and app scaffolding, settings, dependency pin, Git ignore rules, Makefile, setup instructions, implementation plan, and handoff notes. |

I requested a comparison of two ways to match every selected tag. Codex implemented the alternative for the comparison, inspected the SQLite plans and documented the decision to keep the grouped count. [SQL, plans and reproduction steps](docs/all-tags-query.md)
