from django.shortcuts import render

from .forms import ProductSearchForm
from .models import Product
from .queries import filter_products


def product_list(request):
    form = ProductSearchForm(request.GET)
    products = None
    if form.is_valid():
        products = (
            Product.objects.select_related("category")
            .prefetch_related("tags")
            .order_by("name", "pk")
        )
        if form.has_changed():
            products = filter_products(products, **form.cleaned_data)

    return render(
        request, "catalog/product_list.html", {"form": form, "products": products}
    )
