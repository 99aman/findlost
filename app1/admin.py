from django.contrib import admin
from .models import LostOrFound, UploadImage, Category, Subcategory
# Register your models here.

admin.site.register(LostOrFound)
admin.site.register(UploadImage)
admin.site.register(Category)
admin.site.register(Subcategory)