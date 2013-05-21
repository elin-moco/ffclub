# -*- coding: utf-8 -*-
import commonware.log

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.forms import ModelForm, ModelChoiceField
from django.forms.util import ErrorList
from ffclub.upload.models import ImageUpload
from ffclub.event.models import Event

log = commonware.log.getLogger('ffclub')


class ImageUploadForm(ModelForm):
    def __init__(self, user, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=':', empty_permitted=False, instance=None):
        super(ImageUploadForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix,
                                              empty_permitted, instance)
        if data is not None and 'event' in data and data['event'] != '':
            self.event = Event.objects.get(id=data['event'])
        self.user = user
        if user.is_authenticated():
            # Choose from events user created
            userEvents = Event.objects.filter(create_user=user).order_by('-create_time')
            # Default newest event
            userDefaultEvent = userEvents[0] if userEvents.__len__() > 0 else None
            self.hasEvent = userDefaultEvent is not None
            self.fields['event'] = ModelChoiceField(
                queryset=userEvents, label='活動名稱(*)', initial=userDefaultEvent)
            # Set field order as first
            fieldOrder = self.fields.keyOrder
            fieldOrder.pop(fieldOrder.index('event'))
            fieldOrder.insert(0, 'event')

    def save(self, commit=True):
        self.instance.entity_object = self.event
        return super(ImageUploadForm, self).save(commit)

    def clean_image_large(self):
        image = self.cleaned_data.get('image_large', False)
        if image:
            width, height = get_image_dimensions(image)
            if image._size > 5 * 1024 * 1024:
                raise ValidationError('檔案已超過 5MB 上限')
            elif width < 300 or height < 300:
                raise ValidationError('圖片長寬必須大於 300 像素')
            return image
        else:
            raise ValidationError('無法上傳檔案')

    class Meta:
        model = ImageUpload
        fields = ('image_large', 'description')