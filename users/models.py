from django.db import models
from django.contrib.auth.models import User
from PIL import Image #used to resize images on save

#create new profile model with 1-1 relatioship with user
#one user has one profile and vice versa

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #if user deleted,delete profile. If delete profile, don't delete user
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    #method save already exists by default
    #"creating" it let's us make modifications to how it works     
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    