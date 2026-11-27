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
    fixtures = ["sample_catalog"]

    @classmethod
    def setUpTestData(cls):
        cls.outdoors = Category.objects.get(name="Outdoors")
        cls.insulated = Tag.objects.get(name="Insulated")
        cls.steel = Tag.objects.get(name="Stainless steel")
        cls.reusable = Tag.objects.get(name="Reusable")

    def assert_products(self, params, expected):
        response = self.client.get(reverse("product-list"), params)
        self.assertEqual(response.status_code, 200)
        names = [product.name for product in response.context["products"]]
        self.assertEqual(names, sorted(expected))
        for name in expected:
            self.assertContains(response, f"<h3>{name}</h3>", count=1, html=True)
        return response

    def test_blank_and_whitespace_only_searches_show_the_full_catalog(self):
        expected = list(Product.objects.values_list("name", flat=True))
        for params in ({}, {"description": "  ", "category": ""}):
            with self.subTest(params=params):
                response = self.assert_products(params, expected)
                self.assertContains(response, "Category: Outdoors")

    def test_description_matches_one_trimmed_case_insensitive_substring(self):
        self.assert_products({"description": "  SH cOnE  "}, ["Pour-over Coffee Cone"])
        response = self.assert_products({"description": "Pour-over"}, [])
        self.assertContains(response, "No products found.")

    def test_category_alone(self):
        self.assert_products(
            {"category": self.outdoors.pk},
            ["Folding Camp Stool", "Picnic Blanket", "Pocket Trail Map Case", "Trail Coffee Flask"],
        )

    def test_all_selected_tags_are_required_and_repeat_ids_do_not_duplicate_results(self):
        self.assert_products(
            {"tags": [self.insulated.pk]}, ["Trail Coffee Flask", "Commuter Coffee Mug"]
        )
        self.assert_products(
            {"tags": [self.steel.pk, self.reusable.pk, self.steel.pk]},
            ["Trail Coffee Flask", "Pour-over Coffee Cone"],
        )

    def test_combined_filters_and_no_matches(self):
        params = {
            "description": "  COFFEE  ",
            "category": self.outdoors.pk,
            "tags": [self.insulated.pk, self.steel.pk],
        }
        self.assert_products(params, ["Trail Coffee Flask"])
        response = self.assert_products({**params, "description": "map"}, [])
        self.assertContains(response, "No products found.")

    def test_invalid_choices_show_field_errors(self):
        for field in ("tags", "category"):
            with self.subTest(field=field):
                response = self.client.get(reverse("product-list"), {field: "invalid"})
                self.assertIn(field, response.context["form"].errors)
                self.assertContains(response, response.context["form"].errors[field][0])
                self.assertNotContains(response, "<h3>Trail Coffee Flask</h3>", html=True)
