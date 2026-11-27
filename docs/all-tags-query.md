# How the catalog matches every selected tag

The catalog keeps the grouped count in `filter_products`. Filtering the relationship rows to the selected tags before counting lets a product have extra tags. One grouped count expresses the rule for any number of selected tags.

With **Reusable** and **Stainless steel** selected, both implementations below returned **Pour-over Coffee Cone** and **Trail Coffee Flask**, in that order. Products with only one selected tag were excluded.

| Query | Generated SQL, abbreviated | SQLite plan on the sample fixture |
| --- | --- | --- |
| Grouped count | Join the product and relationship tables, apply `WHERE tag_id IN (3, 9)`, group by product, then apply `HAVING COUNT(DISTINCT tag_id) = 2`. | Starts at the relationship table's tag index, then looks up products by primary key. Temporary B-trees handle grouping, distinct counting and output ordering. |
| One existence check per tag | Select products with `WHERE EXISTS (… tag_id = 3) AND EXISTS (… tag_id = 9)`. Each subquery also matches the outer product ID. | Scans products using the name index in display order. Each correlated subquery can probe the unique covering index on the product and tag IDs. |

The grouped plan can start with a small set of relationships when selected tags are rare. The alternative avoids sorting here, but adds a predicate for each selected tag and starts from all candidate products. The comparison covers the tag filter alone on 20 products. It supports keeping the simpler existing implementation. Establishing a speed advantage would require timings at representative catalog sizes and tag frequencies.

## Reproduce the comparison

After loading the sample fixture, run the following from the repository root with the virtual environment active and the Django signing key set. It prints both complete SQL statements, their query plans, and the ordered product names.

```sh
python manage.py shell <<'PY'
from django.db.models import Exists, OuterRef
from catalog.models import Product, Tag
from catalog.queries import filter_products

tags = [Tag.objects.get(name=name) for name in ("Reusable", "Stainless steel")]
products = Product.objects.order_by("name", "pk")
grouped = filter_products(products, description="", category=None, tags=tags)

by_existence = products
for tag in tags:
    membership = Product.tags.through.objects.filter(
        product_id=OuterRef("pk"), tag_id=tag.pk
    )
    by_existence = by_existence.filter(Exists(membership))

for query in (grouped, by_existence):
    print(query.query)
    print(query.explain())
    print([product.name for product in query])
PY
```
