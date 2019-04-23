from django.db import models
from img_params import get_image_params

# Image sizes
LARGE = "877x620"
SMALL = "438x310"

# Create your models here.

class Image(models.Model):
  filename = models.CharField(max_length = 192)
  size = models.CharField(max_length = 7)

  def __init__(self, name = "anon"):
    """ set image params from filename """
    self.params = get_image_params()




@property
def params(self):
    return self._params
