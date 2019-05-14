from django.shortcuts import render
from models import Image

def index(request):
    image_names = map(lambda img: img.name, Image.objects.filter(id__lt=13))
    context = {
        'image_names': image_names
    }
    return render(request, 'fract/index.html', context)