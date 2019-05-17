from django.db import models
from . import img_params

# Image sizes - the two sizes stored in the database
LARGE = "877x620" # stored in static/images/zarg877
SMALL = "438x310" # stored in static/images/zarg438

class Image(models.Model):
  """
  Class to represent and image; the name and size are stored and used
  to fetch the image itself from S3 static storage
  """
  name = models.CharField(max_length = 192)
  size = models.CharField(max_length = 7, default = SMALL)

  def __str__(self):
    return self.name
  
  def params(self):
    """ Get (from the filename)a dictionary of the parameters used to construct the image """
    return img_params.get_image_params(self.name, self.size)

  def name_large(self):
    return self.name.replace(SMALL, LARGE)   



# print('Testing...')
# print(Image('xtsJ2f291C207-pre65-scp-sri-877x620x-0.003710993058573697y-0.0018554965292867376_4266.png', '877x620').params())
