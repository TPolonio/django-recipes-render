from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

#Translating code below:
#When user is saved: send signal
#Signal is received by receiver
#Receiver is the create_profile function
#Create_profile function takes arguments that post_saved signal passed
#So basically if user created => create Profile with user as instance 


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

#After this import signals to apps.py with ready function inside UserConfig