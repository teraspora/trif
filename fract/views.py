from django.shortcuts import render
from .models import Image
# import fract.populate_db
STATIC_IMAGE_DIR = 'images/zarg438/'

def index(request):
    #image_names = map(lambda img: STATIC_IMAGE_DIR + img.name, Image.objects.filter(id__lt=13))
    image_names = map(lambda img: STATIC_IMAGE_DIR + img.name, Image.objects.all())
    context = {
        'image_names': image_names
    }
    return render(request, 'fract/index.html', context)