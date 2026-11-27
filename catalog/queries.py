from django.db.models import Count


def filter_products(products, *, description, category, tags):
    """Apply the validated catalog filters to the supplied product queryset."""
    if description:
        products = products.filter(description__icontains=description)
    if category is not None:
        products = products.filter(category=category)

    tag_ids = [tag.pk for tag in tags]
    if tag_ids:
        # Count only selected tags so a product can also have other tags.
        products = (
            products.filter(tags__in=tag_ids)
            .alias(matching_tags=Count("tags", distinct=True))
            .filter(matching_tags=len(tag_ids))
        )
    return products
