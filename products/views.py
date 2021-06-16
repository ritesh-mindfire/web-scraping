import os
import requests
from slugify import slugify

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from products.models import Product
from products.scrapper import scrap_amazon_books_data
from products import image_downloader


# Create your views here.
def update_product_using_scrap_data():
    scrap_data_lst = scrap_amazon_books_data()
    image_links = []

    for dct in scrap_data_lst:
        title = dct.get('title') or 'N/A'
        slug_field = slugify(title[:200])
        price = dct.get('price', 0)

        link = dct.get('link', '')
        image_links.append(link)
        
        file_name = os.path.basename(link)
        file_path = os.path.join('products', file_name)

        obj = Product.objects.filter(slug=slug_field).first()
        if not obj:
            obj = Product.objects.create(slug=slug_field, title=title, price=price, banner=file_path)
            print('Product created: %s' % obj.id)
        else:
            obj.price = price
            obj.save()
            print('Update price history table.')

        # req = requests.get(link, stream=True)

        # temp_img = NamedTemporaryFile(delete=True)
        # temp_img.write(req.content)
        # temp_img.flush()

        # obj.banner.save(file_name, File(temp_img))
    
    download_dir = os.path.join(settings.MEDIA_ROOT, 'products')
    image_downloader.main(download_dir, image_links)


def dashboard(request):
    return HttpResponse('<h1>It\'s working.. :)</h1>')