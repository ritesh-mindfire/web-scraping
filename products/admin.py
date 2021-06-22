from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from products.models import Product, PriceHistory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'banner_thumb']
    ordering = ['id']

    def banner_thumb(self, obj):
        return format_html("<img src={} alt={} target='_blank' width='100' />".format(obj.banner.url, obj.title))
    banner_thumb.short_description = 'Banner Thumb'


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['product','price']

    # def product_slug(self, obj):
    #     return obj.product
