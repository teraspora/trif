# fract/views.py

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Image
import functools

# ------- only run this to initially populate database with Image objects
if len(Image.objects.all()) == 0:
    import fract.populate_db 

STATIC_SMALL_IMAGE_DIR = 'images/zarg438/'
STATIC_LARGE_IMAGE_DIR = 'images/zarg877/'

class ImageListView(ListView):
    """ Render a List view of all images. """
    model = Image
    paginate_by = 18
    template_name = 'fract/index.html'
    context_object_name = 'image_list'
    ordering = '?'      # random ordering

    def get_context_data(self, **kwargs):
        """
        Get the context and append the STATIC_IMAGE_DIR to it, so we can 
        use this in the template for the image source path.
        """
        context = super(ImageListView, self).get_context_data(**kwargs)
        context['STATIC_SMALL_IMAGE_DIR'] = STATIC_SMALL_IMAGE_DIR
        return context


class LikedImageListView(ListView):
    """ Render a List view of all images liked by this user. """
    paginate_by = 18
    template_name = 'fract/index.html'  # re-use "list all" template for '/likes'
    context_object_name = 'image_list'
    ordering = 'id'      # random ordering

    def get_queryset(self):
        """ Set the queryset to be the set of images liked by this user """
        queryset = self.request.user.profile.liked_images.all()
        return queryset

    def get_context_data(self, **kwargs):
        """
        Get the context and append the STATIC_IMAGE_DIR to it, so we can 
        use this in the template for the image source path, and a 'likes' flag so the
        template knows what heading to use.
        """
        context = super(LikedImageListView, self).get_context_data(**kwargs)
        context['STATIC_SMALL_IMAGE_DIR'] = STATIC_SMALL_IMAGE_DIR
        context['likes'] = True
        return context


class FilteredImageListView(ListView):
    """ Render a List view of all images, filtered by specified parameters. """
    paginate_by = 18
    template_name = 'fract/index.html'  # re-use "list all" template for '/likes'
    context_object_name = 'image_list'
    ordering = 'id'

    def get_queryset(self):
        """ Set the queryset to be the set of all images filtered by the specified parameters """
        EMPTY = ''
        func = self.request.GET.get("func")
        alt_func = self.request.GET.get("alt_func")
        exponent = self.request.GET.get("exponent")
        flavour = self.request.GET.get("flavour")
        queryset = list(filter(lambda img:
            (func == EMPTY or img.params()['func'] == func) and
            (alt_func == EMPTY or img.params()['alt_func'] == alt_func) and
            (exponent == EMPTY or img.params()['power'] == exponent) and
            (flavour == EMPTY or flavour == "*" or img.params()['type'] == flavour),
          Image.objects.all()))
        return queryset

    def get_context_data(self, **kwargs):
        """
        Get the context and append the STATIC_IMAGE_DIR to it, so we can 
        use this in the template for the image source path.
        """
        context = super(FilteredImageListView, self).get_context_data(**kwargs)
        context['STATIC_SMALL_IMAGE_DIR'] = STATIC_SMALL_IMAGE_DIR
        context['filtered'] = True
        return context


class ImageDetailView(DetailView):
    """ Render a detail view of a single image """
    model = Image
    def get_context_data(self, **kwargs):
        """
        Get the context and append the STATIC_IMAGE_DIR to it, so we can 
        use this in the template for the image source path
        """
        context = super(ImageDetailView, self).get_context_data(**kwargs)
        context['STATIC_LARGE_IMAGE_DIR'] = STATIC_LARGE_IMAGE_DIR
        return context

def about(request):
    """ Render the 'About' page. """
    return render(request, 'fract/about.html')
