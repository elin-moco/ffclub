# -*- coding: utf-8 -*-
from cStringIO import StringIO
from django.contrib import auth
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, SuspiciousOperation
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

import commonware.log

from django.utils import simplejson
import facebook
from ffclub.event.models import Campaign, Vote
from ffclub.event.utils import send_photo_report_mail, prefetch_profile_name, prefetch_votes
from ffclub.upload.forms import ImageUploadForm, CampaignImageUploadForm
from ffclub.upload.models import ImageUpload
from ffclub.settings import EVENT_WALL_PHOTOS_PER_PAGE, SITE_URL, FB_APP_NAMESPACE
from ffclub.person.forms import PersonEmailNicknameForm
from ffclub.person.models import Person
from ffclub.upload.utils import generate_share_image

log = commonware.log.getLogger('ffclub')


def wall(request):
    return wall_page(request, 1)


def shareOnFacebook(data, upload):
    if all(key in data.keys() for key in ('shareOnFb', 'fbToken')):
        try:
            graph = facebook.GraphAPI(data['fbToken'])
            image = upload.get_share_image()
            if image.closed:
                image.open()
            graph.put_photo(StringIO(image.read()),
                            upload.description.encode('utf-8') + '\n' + SITE_URL + upload.get_absolute_share_url())
            graph.put_object('me', FB_APP_NAMESPACE + ':upload', picture=SITE_URL + upload.get_absolute_share_url())
        except facebook.GraphAPIError as e:
            log.error(e)


def wall_page(request, page_number=1):
    uploadForm = ImageUploadForm(user=request.user)

    if request.method == 'POST':
        uploadForm = ImageUploadForm(request.user, request.POST, request.FILES)
        if uploadForm.is_valid():
            upload = uploadForm.save(commit=False)
            upload.create_user = auth.get_user(request)
            upload.save()
            shareOnFacebook(request.POST, upload)
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
        data = {'result': 'failed', 'errorMessage': '照片不存在！'}
    except PermissionDenied:
        data = {'result': 'failed', 'errorMessage': '無存取權限！'}

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
        data = {'result': 'failed', 'errorMessage': '照片不存在！'}
    except PermissionDenied:
        data = {'result': 'failed', 'errorMessage': '無存取權限！'}

    json = simplejson.dumps(data)
    return HttpResponse(json, mimetype='application/x-javascript')


def activity_photo_vote(request, type, photo_id):
    try:
        if not request.user.is_active:
            raise PersmissionDenied
        photo = ImageUpload.objects.get(id=photo_id, content_type=ContentType.objects.get(model=type))
        currentUser = auth.get_user(request)
        if Vote.objects.filter(entity_id=photo_id, voter=currentUser,
                               content_type=ContentType.objects.get(model='imageupload')).exists():
            raise SuspiciousOperation
        vote = Vote(entity_object=photo, status='approve', voter=currentUser)
        vote.save()
        data = {'result': 'success', 'message': '投票完成！'}
    except ObjectDoesNotExist:
        data = {'result': 'failed', 'errorMessage': '照片不存在！'}
    except PermissionDenied:
        data = {'result': 'failed', 'errorMessage': '無存取權限！'}
    except SuspiciousOperation:
        data = {'result': 'failed', 'errorMessage': '一張照片只能投一票喔！'}

    json = simplejson.dumps(data)
    return HttpResponse(json, mimetype='application/x-javascript')


def every_moment(request):
    return render(request, 'event/every-moment/index.html')


def every_moment_exceed(request):
    return render(request, 'event/every-moment/exceed.html')


def check_exceed_upload_times(user, slug, max=5):
    if user.is_superuser:
        return False
    campaign = Campaign.objects.get(slug=slug)
    return ImageUpload.objects.filter(entity_id=campaign.id, create_user=user).count() >= max


def every_moment_upload(request):
    uploaded = False
    photo = None
    campaignSlug = 'every-moment'
    if not request.user.is_active:
        uploadForm = CampaignImageUploadForm()
        personForm = PersonEmailNicknameForm()
    elif check_exceed_upload_times(request.user, campaignSlug):
        return redirect('campaign.every.moment.exceed')
    elif request.method == 'POST':
        currentCampaign = Campaign.objects.get(slug=campaignSlug)
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
            generate_share_image(upload, campaignSlug)
            shareOnFacebook(request.POST, upload)
            photo = upload
            uploaded = True
    else:
        uploadForm = CampaignImageUploadForm()
        try:
            personForm = PersonEmailNicknameForm(instance=request.user.get_profile())
        except ObjectDoesNotExist:
            personForm = PersonEmailNicknameForm()
    data = {
        'uploadForm': uploadForm,
        'personForm': personForm,
        'uploaded': uploaded,
        'photo': photo,
    }
    return render(request, 'event/every-moment/upload.html', data)


def every_moment_wall(request):
    return every_moment_wall_page(request, 1)


def campaign_photo(request, slug, photo_id):
    campaign = Campaign.objects.get(slug=slug)
    data = {
        'photo': ImageUpload.objects.get(id=photo_id, entity_id=campaign.id,
                                         content_type=ContentType.objects.get(model='campaign'))
    }
    return render(request, 'event/%s/photo.html' % slug, data)


def every_moment_wall_page(request, page_number=1):
    page_number = int(page_number)
    photoContentTypeId = ContentType.objects.get(model='imageupload').id
    contentTypeId = ContentType.objects.get(model='campaign').id
    entityId = Campaign.objects.get(slug='every-moment').id
    allEventPhotos = list(ImageUpload.objects.raw(
        'SELECT * FROM upload_imageupload WHERE content_type_id=%s AND entity_id=%s '
        'ORDER BY create_user_id=%s DESC, create_time DESC LIMIT %s, %s',
        (contentTypeId, entityId,
         request.user.id if request.user.is_active else -1,
         EVENT_WALL_PHOTOS_PER_PAGE * (page_number - 1), EVENT_WALL_PHOTOS_PER_PAGE))
    )
    prefetch_votes(uploads=allEventPhotos, currentUser=auth.get_user(request))
    prefetch_profile_name(uploads=allEventPhotos)
    return render(request, 'event/every-moment/wall.html', {'event_photos': allEventPhotos})


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
