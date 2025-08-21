from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self): return self.name


class Product(models.Model):
    sku = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price_cents = models.IntegerField()
    currency = models.CharField(max_length=8, default="USD")
    brand = models.CharField(max_length=64, null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    image_url = models.URLField(blank=True)
    attributes = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self): return f"{self.title} ({self.sku})"