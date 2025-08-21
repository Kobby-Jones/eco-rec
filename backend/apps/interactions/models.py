from django.db import models


class Interaction(models.Model):
    TYPES = [
    ("impression","impression"),("view","view"),("click","click"),
    ("add_to_cart","add_to_cart"),("purchase","purchase"),("rating","rating")
    ]
    user = models.ForeignKey("users.AppUser", on_delete=models.CASCADE)
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE)
    type = models.CharField(max_length=32, choices=TYPES)
    value = models.FloatField(null=True, blank=True)
    context = models.JSONField(default=dict)
    ts = models.DateTimeField(auto_now_add=True)