def filter_products(products, *, description, category, tags):
    """Return matching products from the supplied queryset, each appearing once.

    description is a trimmed string, category is a Category or None, and tags
    is a queryset of selected Tag objects. Combine the active filters, matching
    a case-insensitive description substring and every selected tag.
    """
    # The applicant will implement the filtering queryset here.
    return None
