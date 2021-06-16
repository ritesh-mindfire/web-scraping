from rest_framework import serializers
from datetime import date, datetime

from products.models import Product, PriceHistory
from django.contrib.auth import get_user_model
User = get_user_model()


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'updated_at']
        # fields = '__all__'
