from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *


class ImageUploadAdmin(ModelAdmin):
    search_fields = ['image_large', 'description']
    list_filter = ['usage', 'create_time', 'status', 'content_type']

admin.site.register(ImageUpload, ImageUploadAdmin)
