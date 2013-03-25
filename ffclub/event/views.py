from django.contrib import auth
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect

import commonware

from forms import EventForm
from ffclub.upload.forms import ImageUploadForm
from ffclub.upload.models import ImageUpload
from ffclub.person.models import Person


log = commonware.log.getLogger('ffclub')


def wall(request):
    if request.user.is_authenticated() and not Person.objects.filter(user=request.user).exists():
        return redirect('user.register')
    eventForm = EventForm()
    uploadForm = ImageUploadForm()

    if request.method == 'POST':
        eventForm = EventForm(request.POST)
        uploadForm = ImageUploadForm(request.POST, request.FILES)
        if eventForm.is_valid() and uploadForm.is_valid():
            event = eventForm.save(commit=False)
            upload = uploadForm.save(commit=False)
            event.create_user = auth.get_user(request)
            upload.create_user = auth.get_user(request)
            event.save()
            upload.entity_object = event
            upload.save()
            eventForm = EventForm()
            uploadForm = ImageUploadForm()
    allEventPhotos = ImageUpload.objects.filter(content_type=ContentType.objects.get(model='event')).order_by('create_time')
    data = {
        'form': eventForm,
        'upload_form': uploadForm,
        'event_photos': allEventPhotos,
    }

    return render(request, 'event/wall.html', data)
