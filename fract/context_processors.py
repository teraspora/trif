# fract/context_processors.py

# Code adapted from an answer here:
# https://stackoverflow.com/questions/6166055/show-a-form-in-my-template-base-using-django

from .forms import ImageFilterForm

def filter_form(request):
    return { 'filter_form' : ImageFilterForm() }
