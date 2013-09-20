# -*- coding: utf-8 -*-
import commonware.log

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.forms import ModelForm, ModelChoiceField, IntegerField, FloatField, HiddenInput
from django.forms.util import ErrorList
from ffclub.upload.models import ImageUpload
from ffclub.event.models import Event

log = commonware.log.getLogger('ffclub')


class BaseImageUploadForm(ModelForm):

    dragTop = IntegerField(required=False, widget=HiddenInput)
    dragLeft = IntegerField(required=False, widget=HiddenInput)
    frameWidth = IntegerField(required=False, widget=HiddenInput)
    frameHeight = IntegerField(required=False, widget=HiddenInput)

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

    def save(self, commit=True):
        self.instance.dragLeft = self.cleaned_data.get('dragLeft')
        self.instance.dragTop = self.cleaned_data.get('dragTop')
        self.instance.frameWidth = self.cleaned_data.get('frameWidth')
        self.instance.frameHeight = self.cleaned_data.get('frameHeight')
        self.instance.aspectRatio = float(self.instance.frameWidth) / float(self.instance.frameHeight)
        return super(BaseImageUploadForm, self).save(commit)

    class Meta:
        model = ImageUpload
        fields = ['image_large', 'description']


class ImageUploadForm(BaseImageUploadForm):
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


class CampaignImageUploadForm(BaseImageUploadForm):

    def __init__(self, *args, **kwargs):
        super(CampaignImageUploadForm, self).__init__(*args, **kwargs)
        self.fields['image_large'].required = True
        self.fields['description'].required = True
        self.fields['description'].label = '標題'
