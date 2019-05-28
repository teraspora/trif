from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# When user is saved, send a signal to this function, passing the user,
# so a profile is created for the user

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """ Create a user profile. """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """ Save a user profile. """
    instance.profile.save()
