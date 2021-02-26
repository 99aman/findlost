from django.contrib import admin
from .models import LostOrFound, UploadImage, Category, Subcategory, Notification
# Register your models here.

@admin.register(LostOrFound)
class LostOrFoundAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'item_name', 'claimed', 'date_created']
    list_editable = ['claimed']
    list_filter = ['claimed', 'date_created']
    ordering = ['name']
    
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'claimed_by', 'report', 'claimed_on']
    list_filter = ['report', 'date_created']
    date_hierarchy = 'date_created'
    search_fields = ['claimed_by__id', 'claimed_by__username', 'claimed_on__id', 'claimed_on__item_name']

admin.site.register(UploadImage)
admin.site.register(Category)
admin.site.register(Subcategory)