from django.db import models
from . import img_params

# Image sizes
LARGE = "877x620"
SMALL = "438x310"

# Create your models here.

class Image(models.Model):
  name = models.CharField(max_length = 192)
  size = models.CharField(max_length = 7, default = SMALL)

  def __str__(self):
    return self.name

  def __init__(self, name = '', size = SMALL):
    """ 
    set image params from filename
    """
    self.name = name
    self.size = size

  
  def params(self):
    return img_params.get_image_params(self.name, self.size)



print('Testing...')
print(Image('xtsJ2f291C207-pre65-scp-sri-877x620x-0.003710993058573697y-0.0018554965292867376_4266.png', '877x620').params())
