from django.db.models import ProtectedError
from django.test import TestCase

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
