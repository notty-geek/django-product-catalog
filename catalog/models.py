from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="products")

    class Meta:
        indexes = [
            models.Index(fields=["name"], name="product_name_idx"),
            models.Index(fields=["category", "name"], name="product_category_name_idx"),
        ]

    def __str__(self):
        return self.name
