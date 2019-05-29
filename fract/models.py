# fract/models.py

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
    return f'Image { self.id }'
  
  def params(self):
    """ Get (from the filename)a dictionary of the parameters used to construct the image """
    return img_params.get_image_params(self.name, self.size)

  def name_large(self):
    """ Return name of large image associated with this Image object """ 
    return self.name.replace(SMALL, LARGE)

  def num_likes(self):
    """ Return the number of users who have liked this image """
    # profile_set links to the ManyToManyField 'liked_images'
    # in a user's Profile object (see users/models.py)
    return self.profile_set.all().count()   
