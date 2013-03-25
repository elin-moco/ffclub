# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.forms import ModelForm
from ffclub.upload.models import ImageUpload


class ImageUploadForm(ModelForm):

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image._size > 1 * 1024 * 1024:
                raise ValidationError('檔案超已過1MB上限')
            return image
        else:
            raise ValidationError('無法上傳檔案')

    class Meta:
        model = ImageUpload
        fields = ('description', 'image_large')