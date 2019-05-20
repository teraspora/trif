# models.py

from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# from resizeimage import resizeimage

class Profile(models.Model):
    # CASCADE => if user is deleted, then user's profile is also deleted
    # OneToOneField => user has same structure as User model from django.contrib.auth.models
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    liked_images = models.ManyToManyField(fract.Image)

    def __str__(self):
        return f'{self.user.username}\'s profile'

    # def save(self, *args, **kwargs):
    #     img = Image.open(self.image.path)
    #     img = resizeimage.resize_height(img, 128)
    #     self.image = img
    #     super(Profile, self).save(*args, **kwargs)
