from django.db import models

# Create your models here.

class Product(models.Model):
    slug = models.CharField(max_length=256)
    title = models.CharField(max_length=512)
    price = models.FloatField(default=0)
    banner = models.ImageField(upload_to='products')
 