import os
from rest_framework import filters
from rest_framework import generics
from rest_framework import serializers
from celery import shared_task

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.utils.text import slugify
from django_filters.rest_framework import DjangoFilterBackend

from products.models import Product, PriceHistory
from products.serializers import ProductModelSerializer
from products.scrapper import scrap_amazon_books_data
from products import image_downloader


# Create your views here.
@shared_task(name='task_update_product_using_scrap_data')
def task_update_product_using_scrap_data():
    scrap_data_lst = scrap_amazon_books_data()
    print('lenght of scrapped data', len(scrap_data_lst))
    image_links = []

    for dct in scrap_data_lst:
        title = dct.get('title') or 'N/A'
        slug_field = slugify(title[:200])
        price = dct.get('price', 0)

        link = dct.get('link', '')
        
        file_name = os.path.basename(link)
        file_path = os.path.join('products', file_name)

        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, file_path)):
            image_links.append(link)

        obj = Product.objects.filter(slug=slug_field).first()
        if not obj:
            obj = Product.objects.create(slug=slug_field, title=title, price=price, banner=file_path)
            print('Product created: %s' % obj.id)
        else:
            if (price and not obj.price) or (price and obj.price and float(obj.price) != float(price)):
                PriceHistory.objects.create(product=obj, price=price)
            obj.price = price
            obj.save()

            print('Update price and price history table.')

        # req = requests.get(link, stream=True)

        # temp_img = NamedTemporaryFile(delete=True)
        # temp_img.write(req.content)
        # temp_img.flush()

        # obj.banner.save(file_name, File(temp_img))
    
    download_dir = os.path.join(settings.MEDIA_ROOT, 'products')
    image_downloader.main(download_dir, image_links)


def dashboard(request):
    ctx = {}
    return render(request, 'dashboard.html', context=ctx)


class PriceFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see price between a range
    """
    def filter_queryset(self, request, queryset, view):
        price_lt = request.query_params.get('price_lt')
        price_gt = request.query_params.get('price_gt')
        if price_lt and not price_lt.isnumeric():
            raise serializers.ValidationError({'price_lt': "Enter a number."})
        if price_gt and not price_gt.isnumeric():
            raise serializers.ValidationError({'price_gt': "Enter a number."})
        if price_lt:
            queryset = queryset.filter(price__lt=price_lt)
        if price_gt:
            queryset = queryset.filter(price__gt=price_gt)
        return queryset


class ProductsList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, PriceFilterBackend]
    search_fields = ['title',]
    ordering_fields = ['title', 'price', 'updated_at']
    filterset_fields = ['price',]


