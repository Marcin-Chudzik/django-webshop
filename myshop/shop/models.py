from django.db import models
from django.urls import reverse


class Category(models.Model):
    """
    A model representing a category of products in the online shop.

    Attributes:
        name (str): The name of the category.
        slug (str): A unique slug used in the URL to identify the category.

    Meta:
        ordering (tuple): The default ordering for the categories (by name).
        verbose_name (str): The singular name of the category (for display purposes).
        verbose_name_plural (str): The plural name of the category (for display purposes).

    Methods:
        __str__(): Returns the string representation of the category (its name).
        get_absolute_url(): Returns the URL of the page displaying the products in the category.
    """
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    """
    Represents a product that is available for purchase in the online store.

    Fields:
        category (ForeignKey): The category that the product belongs to.
        name (CharField): The name of the product.
        slug (SlugField): The URL-friendly slug for the product.
        image (ImageField): An image of the product.
        description (TextField): A detailed description of the product.
        price (DecimalField): The price of the product.
        available (BooleanField): Indicates whether the product is currently available for purchase.
        created (DateTimeField): The date and time the product was created.
        updated (DateTimeField): The date and time the product was last updated.

    Meta:
        ordering (tuple): The default ordering for the model.
        verbose_name (str): The singular name of the model.
        verbose_name_plural (str): The plural name of the model.
        index_together (tuple): Specifies the database indexes for the model.

    Methods:
        __str__(): Returns a string representation of the product.
        get_absolute_url(): Returns the absolute URL for the product detail view.
    """
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
