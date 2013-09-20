# -*- coding: utf-8 -*-
from cStringIO import StringIO
from django.contrib import auth
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

import commonware.log

from django.utils import simplejson
import facebook
from ffclub.event.models import Campaign
from ffclub.event.utils import send_photo_report_mail
from ffclub.upload.forms import ImageUploadForm, CampaignImageUploadForm
from ffclub.upload.models import ImageUpload
from ffclub.settings import EVENT_WALL_PHOTOS_PER_PAGE, SITE_URL, FB_APP_NAMESPACE
from ffclub.person.forms import PersonEmailNicknameForm

log = commonware.log.getLogger('ffclub')


def wall(request):
    return wall_page(request, 1)


def shareOnFacebook(data, upload):
    if all(key in data.keys() for key in ('shareOnFb', 'fbToken')):
        try:
            graph = facebook.GraphAPI(data['fbToken'])
            upload.image_large.open()
            graph.put_photo(StringIO(upload.image_large.read()), upload.description.encode('utf-8'))
            graph.put_object('me', FB_APP_NAMESPACE + ':upload', picture=SITE_URL + upload.get_absolute_url())
        except facebook.GraphAPIError as e:
            log.error(e)


def wall_page(request, page_number=1):
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
            shareOnFacebook(request.POST, upload)
            # eventForm = EventForm()
            uploadForm = ImageUploadForm(user=request.user)
    allEventPhotos = ImageUpload.objects.filter(
        content_type=ContentType.objects.get(model='event')
    ).exclude(status='spam').order_by('-create_time').prefetch_related('create_user', 'create_user__person')
    for eventPhoto in allEventPhotos:
        try:
            eventPhoto.create_username = eventPhoto.create_user.person.fullname
        except ObjectDoesNotExist:
            eventPhoto.create_username = ''
    paginator = Paginator(allEventPhotos, EVENT_WALL_PHOTOS_PER_PAGE)
    data = {
        # 'form': eventForm,
        'upload_form': uploadForm,
        'event_photos': paginator.page(page_number),
    }

    return render(request, 'event/wall.html', data)


def activity_photo(request, type, photo_id):
    data = {
        'photo': ImageUpload.objects.get(id=photo_id, content_type=ContentType.objects.get(model=type))
    }
    return render(request, 'event/event_photo.html', data)


def activity_photo_remove(request, type, photo_id):
    try:
        photo = ImageUpload.objects.get(id=photo_id, content_type=ContentType.objects.get(model=type))
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


def activity_photo_report(request, type, photo_id):
    try:
        photo = ImageUpload.objects.get(id=photo_id, content_type=ContentType.objects.get(model=type))
        if not request.user.is_active:
            raise PermissionDenied
        photo.status = 'reported'
        photo.save()
        try:
            from_name = auth.get_user(request).get_profile().fullname
        except ObjectDoesNotExist:
            from_name = ''
        try:
            to_name = photo.create_user.get_profile().fullname
        except ObjectDoesNotExist:
            to_name = ''
        send_photo_report_mail(from_name, to_name, photo_id)
        data = {'result': 'success'}
    except ObjectDoesNotExist:
        data = {'result': 'failed', 'error': '照片不存在！'}
    except PermissionDenied:
        data = {'result': 'failed', 'error': '無存取權限！'}

    json = simplejson.dumps(data)
    return HttpResponse(json, mimetype='application/x-javascript')


def every_moment(request):
    return render(request, 'event/every-moment/index.html')


def every_moment_upload(request):
    if request.method == 'POST':
        currentCampaign = Campaign.objects.get(slug='every-moment')
        currentUser = auth.get_user(request)
        uploadForm = CampaignImageUploadForm(request.POST, request.FILES)
        try:
            personForm = PersonEmailNicknameForm(request.POST, instance=currentUser.get_profile())
        except ObjectDoesNotExist:
            personForm = PersonEmailNicknameForm(request.POST)
        if all([uploadForm.is_valid(), personForm.is_valid()]):
            person = personForm.save(commit=False)
            if not hasattr(person, 'user'):
                person.user = currentUser
            upload = uploadForm.save(commit=False)
            upload.create_user = currentUser
            upload.entity_object = currentCampaign
            person.save()
            upload.save()
            shareOnFacebook(request.POST, upload)
            if request.user.is_active:
                uploadForm = CampaignImageUploadForm()
                try:
                    personForm = PersonEmailNicknameForm(instance=request.user.get_profile())
                except ObjectDoesNotExist:
                    personForm = PersonEmailNicknameForm()
    else:
        if request.user.is_active:
            uploadForm = CampaignImageUploadForm()
            try:
                personForm = PersonEmailNicknameForm(instance=request.user.get_profile())
            except ObjectDoesNotExist:
                personForm = PersonEmailNicknameForm()
    data = {
        'uploadForm': uploadForm,
        'personForm': personForm,
    }
    return render(request, 'event/every-moment/upload.html', data)


def every_moment_wall(request):
    return every_moment_wall_page(request, 1)


def every_moment_wall_page(request, page_number=1):
    allEventPhotos = ImageUpload.objects.filter(
        content_type=ContentType.objects.get(model='campaign'), entity_id=Campaign.objects.get(slug='every-moment').id
    ).order_by('-create_time').prefetch_related('create_user', 'create_user__person')
    for eventPhoto in allEventPhotos:
        try:
            eventPhoto.create_username = eventPhoto.create_user.person.fullname
        except ObjectDoesNotExist:
            eventPhoto.create_username = ''
    paginator = Paginator(allEventPhotos, EVENT_WALL_PHOTOS_PER_PAGE)
    return render(request, 'event/every-moment/wall.html', {'event_photos': paginator.page(page_number)})


def attack_on_web(request):
    return render(request, 'event/attack-on-web/index.html')


def prizes(request):
    return render(request, 'event/attack-on-web/prizes.html')


def apply(request):
    return render(request, 'event/attack-on-web/apply.html')


def demo(request):
    return render(request, 'event/attack-on-web/demo.html')


def microfilm(request):
    return render(request, 'event/attack-on-web/microfilm.html')
