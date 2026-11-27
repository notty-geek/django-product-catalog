from unittest.mock import patch

from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse

from .models import Category, Product, Tag


class CatalogRelationshipTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Kitchen")
        cls.product = Product.objects.create(
            name="Mug", description="Stoneware mug", category=cls.category
        )

    def test_category_can_be_deleted_after_its_product_is_reassigned(self):
        with self.assertRaises(ProtectedError):
            self.category.delete()

        replacement = Category.objects.create(name="Tableware")
        self.product.category = replacement
        self.product.save()
        self.category.delete()

        self.product.refresh_from_db()
        self.assertEqual(self.product.category, replacement)

    def test_deleting_shared_tag_preserves_products_and_their_other_tags(self):
        bowl = Product.objects.create(
            name="Bowl", description="Stoneware bowl", category=self.category
        )
        shared_tag = Tag.objects.create(name="Stoneware")
        other_tag = Tag.objects.create(name="Gift")
        self.product.tags.add(shared_tag, other_tag)
        bowl.tags.add(shared_tag)

        shared_tag.delete()

        self.assertCountEqual(self.category.products.all(), [self.product, bowl])
        self.assertEqual(list(self.product.tags.all()), [other_tag])
        self.assertFalse(bowl.tags.exists())


class ProductListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Outdoors")
        cls.flask = Product.objects.create(
            name="Trail Flask", description="For hot coffee", category=cls.category
        )
        cls.cone = Product.objects.create(
            name="Coffee Cone", description="Mesh dripper", category=cls.category
        )
        cls.tags = [Tag.objects.create(name=name) for name in ("Insulated", "Reusable")]
        cls.flask.tags.set(cls.tags)

    @patch("catalog.views.filter_products")
    def test_blank_search_lists_each_product_and_its_details(self, filter_products):
        for params in ({}, {"description": "  ", "category": ""}):
            with self.subTest(params=params):
                response = self.client.get(reverse("product-list"), params)
                self.assertContains(response, "<h3>Trail Flask</h3>", count=1, html=True)
                self.assertContains(response, "<h3>Coffee Cone</h3>", count=1, html=True)
                self.assertContains(response, "For hot coffee")
                self.assertContains(response, "Category: Outdoors")
                self.assertContains(response, "Tags:")
        filter_products.assert_not_called()

    @patch("catalog.views.filter_products")
    def test_valid_filters_pass_cleaned_values_and_render_returned_products(self, filter_products):
        filter_products.return_value = [self.flask]
        response = self.client.get(reverse("product-list"), {
            "description": "  COFFEE  ",
            "category": self.category.pk,
            "tags": [tag.pk for tag in self.tags],
        })
        filter_products.assert_called_once()
        self.assertEqual(filter_products.call_args.args[0].model, Product)
        values = filter_products.call_args.kwargs
        self.assertEqual(values["description"], "COFFEE")
        self.assertEqual(values["category"], self.category)
        self.assertCountEqual(values["tags"], self.tags)
        self.assertContains(response, "<h3>Trail Flask</h3>", html=True)
        self.assertNotContains(response, "<h3>Coffee Cone</h3>", html=True)

    @patch("catalog.views.filter_products", return_value=[])
    def test_valid_search_can_return_no_matches(self, filter_products):
        response = self.client.get(reverse("product-list"), {"description": "missing"})
        self.assertContains(response, "No products found.")
        self.assertNotContains(response, "<h3>Trail Flask</h3>", html=True)

    @patch("catalog.views.filter_products")
    def test_invalid_choices_show_field_errors(self, filter_products):
        for field in ("tags", "category"):
            with self.subTest(field=field):
                response = self.client.get(reverse("product-list"), {field: "invalid"})
                self.assertIn(field, response.context["form"].errors)
                self.assertContains(response, response.context["form"].errors[field][0])
                self.assertNotContains(response, "<h3>Trail Flask</h3>", html=True)
        filter_products.assert_not_called()
