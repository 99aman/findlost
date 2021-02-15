from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class LostOrFound(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    item_name = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    subcategory = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.PositiveIntegerField(default=999-999-999)
    pin_code = models.PositiveIntegerField(default=100011)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)
    select = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(max_length=500, help_text='write in short what you lost/found', blank=True, null=True)

    def __str__(self):
        return f'{self.item_name}'


class UploadImage(models.Model):
    lostfound = models.ForeignKey(LostOrFound, on_delete=models.CASCADE, blank=True, null=True)
    upload_image = models.ImageField('img_upload/', blank=True, null=True)

    def __str__(self):
        return f'{self.id}'

class Category(models.Model):
    lostorfound = models.ForeignKey(LostOrFound, blank=True, null=True, on_delete=models.CASCADE, related_name='get_category')
    category_name = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f'{self.category_name}'

class Subcategory(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    lostorfound = models.ForeignKey(LostOrFound, blank=True, null=True, on_delete=models.CASCADE, related_name='get_subcategory')
    subcategory_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.subcategory_name}'


