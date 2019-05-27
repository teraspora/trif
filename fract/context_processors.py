# context_processors.py

from .forms import ImageFilterForm

def filter_form(request):
return {
     'filter_form' : ImageFilterForm()
}