from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'title', 'banner_thumb']

    def banner_thumb(self, obj):
        return format_html("<img src={} alt={} target='_blank' width='100' />".format(obj.banner.url, obj.title))
    banner_thumb.short_description = 'Banner Thumb'