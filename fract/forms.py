from django import forms
from .models import Image

class ImageFilterForm(forms.Form):
    all_imgs = Image.objects.all()
    FLAVOURS = (('M', 'Mandelbrot'), ('J', 'Julia'))
    power_max = max([int(img.params()['power']) for img in imgs])
    f_min = min([int(img.params()['func']) for img in imgs])
    f_max = max([int(img.params()['func']) for img in imgs])
    g_min = min([int(img.params()['alt_func']) for img in imgs])
    g_max = max([int(img.params()['alt_func']) for img in imgs])

    func = forms.IntegerField(label='Function', min_value=f_min, max_value=f_max)
    alt_func = forms.IntegerField(label='Alt-function', min_value=g_min, max_value=g_max)   
    func = forms.IntegerField(label='Exponent', min_value=1, max_value=power_max)
    flavour = forms.CharField(label='Type', max_length=1, choices=FLAVOURS)

# sample code for reference: remove before submission/production
#     name = forms.CharField(max_length=100)
#     title = forms.CharField(
#         max_length=3,
#         widget=forms.Select(choices=TITLE_CHOICES),
#     )
#     birth_date = forms.DateField(required=False)

# class BookForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all())