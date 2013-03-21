from django.forms import ModelForm
from ffclub.upload.models import ImageUpload


class ImageUploadForm(ModelForm):
    class Meta:
        model = ImageUpload