from django.shortcuts import render
from django.views.generic import ListView
from .models import Image

# ------- only run this to initially populate database with Image objects
if len(Image.objects.all()) == 0:
    import fract.populate_db 

STATIC_IMAGE_DIR = 'images/zarg438/'

# OLD view-function, replaced by class-based view below
# def index(request):
#     #image_names = map(lambda img: STATIC_IMAGE_DIR + img.name, Image.objects.filter(id__lt=13)) # for testing

#     # Get image data as a list of tuples like ('xtsM2f101C431-pre167-438x310x0.0y0.0_6594.png', 74)
#     image_data = map(lambda img: (STATIC_IMAGE_DIR + img.name, img.id), Image.objects.all())
#     context = {
#         'image_data': image_data
#     }
#     return render(request, 'fract/index.html', context)

class ImageListView(ListView):
    model = Image
    template_name = 'fract/index.html'
    context_object_name = 'image_list'

    def get_context_data(self, **kwargs):
        context = super(ImageListView, self).get_context_data(**kwargs)
        context['STATIC_IMAGE_DIR'] = STATIC_IMAGE_DIR
        return context

