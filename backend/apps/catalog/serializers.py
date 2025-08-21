from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","sku","title","description","price_cents","currency","brand","image_url","attributes","category_id"]