import csv
from django.core.management.base import BaseCommand
from apps.users.models import AppUser
from apps.catalog.models import Product, Category
from apps.interactions.models import Interaction
from django.db import transaction


USERS = [
{"id":1,"email":"alice@example.com"},
{"id":2,"email":"bob@example.com"},
]
CATEGORIES = [
{"id":11,"name":"Shoes"},
{"id":12,"name":"Tops"},
{"id":13,"name":"Electronics"},
]
PRODUCTS = [
{"id":101,"sku":"SKU101","title":"Blue Sneakers","price_cents":7999,"currency":"USD","brand":"RunX","category_id":11,"image_url":"https://picsum.photos/seed/101/400"},
{"id":102,"sku":"SKU102","title":"Red Hoodie","price_cents":5599,"currency":"USD","brand":"ClothCo","category_id":12,"image_url":"https://picsum.photos/seed/102/400"},
{"id":103,"sku":"SKU103","title":"Wireless Earbuds","price_cents":9999,"currency":"USD","brand":"Sonic","category_id":13,"image_url":"https://picsum.photos/seed/103/400"},
]
INTERACTIONS = [
{"user_id":1,"product_id":101,"type":"view"},
{"user_id":1,"product_id":101,"type":"click"},
{"user_id":1,"product_id":103,"type":"view"},
{"user_id":2,"product_id":102,"type":"view"},
{"user_id":2,"product_id":102,"type":"add_to_cart"},
{"user_id":2,"product_id":102,"type":"purchase","value":5599},
]

class Command(BaseCommand):
    help = "Load sample users/products/interactions"


    @transaction.atomic
    def handle(self, *args, **kwargs):
        for u in USERS:
            AppUser.objects.update_or_create(id=u["id"], defaults={"email":u["email"]})
        for c in CATEGORIES:
            Category.objects.update_or_create(id=c["id"], defaults={"name":c["name"]})
        for p in PRODUCTS:
            Product.objects.update_or_create(
            id=p["id"],
            defaults={k:v for k,v in p.items() if k!="id"}
            )
        for r in INTERACTIONS:
            Interaction.objects.create(**r)
        self.stdout.write(self.style.SUCCESS("Sample data loaded."))