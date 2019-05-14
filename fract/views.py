from django.shortcuts import render
from .models import Image
    
STATIC_IMAGE_DIR = 'images/zarg438/'

def index(request):
    image_names = map(lambda img: STATIC_IMAGE_DIR + img.name, Image.objects.filter(id__lt=13))
    context = {
        'image_names': image_names
    }
    return render(request, 'fract/index.html', context)