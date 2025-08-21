from django.db import models


class AppUser(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    country_code = models.CharField(max_length=8, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=16, null=True, blank=True)
    meta = models.JSONField(default=dict)


    def __str__(self):
        return self.email