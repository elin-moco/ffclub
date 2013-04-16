# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

import commonware

# from forms import EventForm
from django.utils import simplejson
from ffclub.upload.forms import ImageUploadForm
from ffclub.upload.models import ImageUpload
from ffclub.person.models import Person
from ffclub.settings import EVENT_WALL_PHOTOS_PER_PAGE, FB_APP_ID

log = commonware.log.getLogger('ffclub')


def wall(request):
    return wall_page(request, 1)


def wall_page(request, page_number=1):
    if request.user.is_authenticated() and not Person.objects.filter(user=request.user).exists():
        return redirect('user.register')
        # eventForm = EventForm()
    uploadForm = ImageUploadForm(user=request.user)

    if request.method == 'POST':
        # eventForm = EventForm(request.POST)
        uploadForm = ImageUploadForm(request.user, request.POST, request.FILES)
        if uploadForm.is_valid():  # and eventForm.is_valid():
            # event = eventForm.save(commit=False)
            upload = uploadForm.save(commit=False)
            # event.create_user = auth.get_user(request)
            upload.create_user = auth.get_user(request)
            # event.save()
            # upload.entity_object = event
            upload.save()
            # eventForm = EventForm()
            uploadForm = ImageUploadForm(user=request.user)
    allEventPhotos = ImageUpload.objects.filter(
        content_type=ContentType.objects.get(model='event')).order_by('-create_time')
    paginator = Paginator(allEventPhotos, EVENT_WALL_PHOTOS_PER_PAGE)
    data = {
        # 'form': eventForm,
        'upload_form': uploadForm,
        'event_photos': paginator.page(page_number),
        'FB_APP_ID': FB_APP_ID,
    }

    return render(request, 'event/wall.html', data)


def event_photo(request, photo_id):
    data = {
        'photo': ImageUpload.objects.get(id=photo_id, content_type=ContentType.objects.get(model='event'))
    }
    return render(request, 'event/event_photo.html', data)


def event_photo_remove(request, photo_id):
    try:
        photo = ImageUpload.objects.get(id=photo_id, content_type=ContentType.objects.get(model='event'))
        if request.user != photo.create_user:
            raise PermissionDenied
        photo.delete()
        data = {'result': 'success'}
    except ObjectDoesNotExist:
        data = {'result': 'failed', 'error': '照片不存在！'}
    except PermissionDenied:
        data = {'result': 'failed', 'error': '無存取權限！'}

    json = simplejson.dumps(data)
    return HttpResponse(json, mimetype='application/x-javascript')


def event_photo_report(request, photo_id):
    try:
        photo = ImageUpload.objects.get(id=photo_id, content_type=ContentType.objects.get(model='event'))
        if not request.user.is_active:
            raise PermissionDenied
        photo.status = 'reported'
        photo.save()
        data = {'result': 'success'}
    except ObjectDoesNotExist:
        data = {'result': 'failed', 'error': '照片不存在！'}
    except PermissionDenied:
        data = {'result': 'failed', 'error': '無存取權限！'}

    json = simplejson.dumps(data)
    return HttpResponse(json, mimetype='application/x-javascript')