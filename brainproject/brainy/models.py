from django.db import models 
from django.db.models import F
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.dispatch import receiver
from django.shortcuts import render
import numpy as np

GENDER=(
    ("Male","M",),
    ("Female","F"),
)
CATEGORY=(
    ("glioma","G"),
    ("meningioma","M"),
    ("notumor","N"),
    ("pituitary","P")
)

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)  
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True,
        verbose_name=_('groups'),
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True,
        verbose_name=_('user permissions'),
        help_text=_('Specific permissions for this user.'),
    )
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=GENDER,max_length=20,blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username

    def get_phone_number(self):
        return self.user.phone_number if self.user else None

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class ScanHistory(models.Model):
    mri = models.ImageField(upload_to='scans/', null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField()
    Model1 = models.TextField(blank=True)
    Model2 = models.TextField(blank=True)
    Model3 = models.TextField(blank=True)
    Model4 = models.TextField(blank=True)
    Model5 = models.TextField(blank=True)
    Result = models.CharField(max_length=30, choices=CATEGORY)

    def __str__(self):
        return str(self.profile)

    @staticmethod
    def getUser(user):
        return ScanHistory.objects.filter(profile__user=user)

    def get_predicted_result_label(self):
        category_dict = dict(CATEGORY)
        return category_dict.get(self.Result)

    def get_prediction_category(self, prediction_array):
        max_value = None
        max_index = None
        predictions_array = np.fromstring(prediction_array, sep=',')  # Deserialize
        local_max_value = np.max(predictions_array)
        if max_value is None or local_max_value > max_value:  # Update max values
            max_value = local_max_value
            max_index = np.argmax(predictions_array)
        if max_index is not None:
            return CATEGORY[max_index][0]  # Return category code based on final max_index
        else:
            return None
