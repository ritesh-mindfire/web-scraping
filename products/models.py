from django.db import models

# Create your models here.

class Product(models.Model):
    slug = models.CharField(max_length=256, unique=True, db_index=True)
    title = models.CharField(max_length=512)
    price = models.FloatField(default=0, null= True)
    banner = models.ImageField(upload_to='products')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug


class PriceHistory(models.Model):
    price = models.FloatField(default=0)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='prices')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
