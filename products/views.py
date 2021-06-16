import os
from rest_framework import filters
from rest_framework import generics

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.utils.text import slugify
import django_filters.rest_framework


from products.models import Product, PriceHistory
from products.scrapper import scrap_amazon_books_data
from products import image_downloader
from products.serializers import ProductModelSerializer

# Create your views here.
def update_product_using_scrap_data():
    scrap_data_lst = scrap_amazon_books_data()
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
            if float(obj.price) != float(price):
                obj.price = price
                obj.save() 
                PriceHistory.objects.create(product=obj, price=price)
            print('Update price and price history table.')

        # req = requests.get(link, stream=True)

        # temp_img = NamedTemporaryFile(delete=True)
        # temp_img.write(req.content)
        # temp_img.flush()

        # obj.banner.save(file_name, File(temp_img))
    
    download_dir = os.path.join(settings.MEDIA_ROOT, 'products')
    image_downloader.main(download_dir, image_links)


def dashboard(request):
    return HttpResponse('<h1>It\'s working.. :)</h1>')

class ProductsList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title',]
    ordering_fields = ['title', 'price', 'updated_at']


    # filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # search_fields = ['name', 'country']
    # filterset_fields = ['name', 'country']
