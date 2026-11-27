from django import forms

from .models import Category, Tag


class ProductSearchForm(forms.Form):
    description = forms.CharField(label="Search descriptions", required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.order_by("name"),
        empty_label="All categories",
        required=False,
    )
    tags = forms.ModelMultipleChoiceField(
        label="Match all selected tags",
        queryset=Tag.objects.order_by("name"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
