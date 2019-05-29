# users/models.py

from django.db import models
from django.contrib.auth.models import User
from fract.models import Image

class Profile(models.Model):
    """ Represents a user's profile, including profile picture. """
    # CASCADE => if user is deleted, then user's profile is also deleted
    # OneToOneField => user has same structure as User model from django.contrib.auth.models
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    liked_images = models.ManyToManyField(Image)

    def __str__(self):
        return f'{self.user.username}\'s profile'
