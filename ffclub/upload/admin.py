from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *


class ImageUploadInline(generic.GenericTabularInline):
    model = ImageUpload
    ct_fk_field = 'entity_id'
    extra = 0


class ImageUploadAdmin(ModelAdmin):
    search_fields = ['image_large', 'description']
    list_filter = ['usage', 'create_time', 'status', 'content_type']

admin.site.register(ImageUpload, ImageUploadAdmin)
