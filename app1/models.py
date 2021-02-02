from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class LostOrFound(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    item_name = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.PositiveIntegerField(default=999-999-999)
    pin_number = models.PositiveIntegerField(default=100011)
    item_image = models.ImageField('img_upload/', blank=True, null=True)
    select = models.CharField(max_length=10, blank=True, null=True)
    category = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(max_length=500, help_text='write in short what you lost/found')

    def __str__(self):
        return f'{self.item_name}'

