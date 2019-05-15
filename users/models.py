from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # CASCADE => if user is deleted, then user's profile is also deleted
    # OneToOneField => user has same structure as User model from django.contrib.auth.models
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'Profile for {self.user.username}.'
