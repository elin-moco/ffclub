# -*- coding: utf-8 -*-
from cStringIO import StringIO
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, SuspiciousOperation
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
import commonware.log
import random
import json
from django.utils.encoding import force_unicode
import facebook
from ffclub.event.models import Activity, Event, Campaign, Vote, Video, Participation, Award, DemoApp, Price
from ffclub.event.utils import send_photo_report_mail, prefetch_profile_name, prefetch_votes, weighted_sample, generate_claim_code, generate_10years_ticket, get_1day_range
from ffclub.upload.forms import ImageUploadForm, CampaignImageUploadForm
from ffclub.upload.models import ImageUpload
from ffclub.settings import EVENT_WALL_PHOTOS_PER_PAGE, SITE_URL, FB_APP_NAMESPACE
from ffclub.person.forms import PersonForm, PersonEmailNicknameForm, AwardClaimForm
from ffclub.person.models import Person
from ffclub.person.views import genderMap
from ffclub.upload.utils import generate_share_image
from social_auth.db.django_models import UserSocialAuth
from django.db.models import Q
from commonware.response.decorators import xframe_allow
from django.views.decorators.csrf import csrf_exempt
from ffclub.base.decorators import cors_allow, enable_jsonp
from ffclub.settings import MOCO_URL, API_SECRET
from datetime import datetime


log = commonware.log.getLogger('ffclub')

everyMomentCampaignSlug = 'every-moment'
lanternFestivalCampaignSlug = 'lantern-festival'
chineseValentinesDayCampaignSlug = 'chinese-valentines-day'
tenYearsCampaignSlug = '10years'
review2014CampaignSlug = '2014review'


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
        'event_photos': paginator.page(page_number) if paginator.num_pages >= page_number else (),
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

    response = json.dumps(data)
    return HttpResponse(response, mimetype='application/x-javascript')


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

    response = json.dumps(data)
    return HttpResponse(response, mimetype='application/x-javascript')


def activity_photo_vote(request, type, photo_id):
    try:
        if not request.user.is_active:
            raise PermissionDenied
        photo = ImageUpload.objects.get(id=photo_id, content_type=ContentType.objects.get(model=type))
        if not 'voting' == photo.entity_object.status:
            raise PermissionDenied
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

    response = json.dumps(data)
    return HttpResponse(response, mimetype='application/x-javascript')


def generic_vote(request, type, id):
    try:
        if not request.user.is_active:
            raise PermissionDenied
        currentUser = auth.get_user(request)
        contentType = ContentType.objects.get(model=type)
        if Vote.objects.filter(entity_id=id, voter=currentUser,
                               content_type=contentType).exists():
            raise SuspiciousOperation
        vote = Vote(entity_id=id, content_type=contentType, status='approve', voter=currentUser)
        vote.save()
        data = {'result': 'success', 'message': '投票完成！'}
    except PermissionDenied:
        data = {'result': 'failed', 'errorMessage': '無存取權限！'}
    except SuspiciousOperation:
        data = {'result': 'failed', 'errorMessage': '一部微電影只能投一票喔！'}

    response = json.dumps(data)
    return HttpResponse(response, mimetype='application/x-javascript')


def every_moment(request):
    currentCampaign = Campaign.objects.get(slug=everyMomentCampaignSlug)
    return render(request, 'event/every-moment/index.html', {'campaign': currentCampaign})


def every_moment_exceed(request):
    currentCampaign = Campaign.objects.get(slug=everyMomentCampaignSlug)
    return render(request, 'event/every-moment/exceed.html', {'campaign': currentCampaign})


def every_moment_result(request):
    currentCampaign = Campaign.objects.get(slug=everyMomentCampaignSlug, status='result')
    popularAwards = list(Award.objects.filter(name=u'最高人氣獎', activity=currentCampaign).prefetch_related('winner', 'winner__person').order_by('order'))
    if len(popularAwards) > 0:
        champion = popularAwards[0]
        champion.winner.fullname = champion.winner.person.fullname if hasattr(champion.winner, 'person') else '%s %s' % (champion.winner.last_name, champion.winner.first_name)
    else:
        champion = {}
    if len(popularAwards) > 1:
        popularAwards = popularAwards[1:]
        for popularAward in popularAwards:
            popularAward.winner.fullname = popularAward.winner.person.fullname if hasattr(popularAward.winner, 'person') else ('%s %s' % (popularAward.winner.last_name, popularAward.winner.first_name))
    else:
        popularAwards = []
    luckyAwards = Award.objects.filter(name=u'投票幸運獎', activity=currentCampaign).prefetch_related('winner', 'winner__person').order_by('order')
    for luckyAward in luckyAwards:
        luckyAward.winner.fullname = luckyAward.winner.person.fullname if hasattr(luckyAward.winner, 'person') else ('%s %s' % (luckyAward.winner.last_name, luckyAward.winner.first_name))
    return render(request, 'event/every-moment/result.html',
                  {
                      'campaign': currentCampaign,
                      'champion': champion,
                      'popularAwards': popularAwards,
                      'luckyAwards': luckyAwards,
                  })


def check_exceed_upload_times(user, campaign, max=5):
    if user.is_superuser:
        return False
    return ImageUpload.objects.filter(entity_id=campaign.id, create_user=user).count() >= max


def every_moment_upload(request):
    currentCampaign = Campaign.objects.get(slug=everyMomentCampaignSlug)
    if not 'running' == currentCampaign.status:
        raise PermissionDenied
    uploaded = False
    photo = None
    if not request.user.is_active:
        uploadForm = CampaignImageUploadForm()
        personForm = PersonEmailNicknameForm()
    elif check_exceed_upload_times(request.user, currentCampaign):
        return redirect('campaign.every.moment.exceed')
    elif request.method == 'POST':
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
            generate_share_image(upload, everyMomentCampaignSlug)
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
        'campaign': currentCampaign,
        'uploadForm': uploadForm,
        'personForm': personForm,
        'uploaded': uploaded,
        'photo': photo,
    }
    return render(request, 'event/every-moment/upload.html', data)


def every_moment_wall(request):
    return every_moment_wall_page(request, 1)


def campaign_photo(request, slug, photo_id):
    currentCampaign = Campaign.objects.get(slug=everyMomentCampaignSlug)
    data = {
        'campaign': currentCampaign,
        'photo': ImageUpload.objects.get(id=photo_id, entity_id=currentCampaign.id,
                                         content_type=ContentType.objects.get(model='campaign'))
    }
    return render(request, 'event/%s/photo.html' % slug, data)


def every_moment_wall_page(request, page_number=1):
    currentCampaign = Campaign.objects.get(slug=everyMomentCampaignSlug)
    page_number = int(page_number)
    photoContentType = ContentType.objects.get(model='imageupload')
    photoContentTypeId = photoContentType.id
    contentTypeId = ContentType.objects.get(model='campaign').id
    entityId = currentCampaign.id
    orderByClause = ('RAND(%d)' % (request.user.id if request.user.is_active else -1)) \
        if currentCampaign.status == 'voting' else 'create_time'
    allEventPhotos = list(ImageUpload.objects.raw(
        'SELECT * FROM upload_imageupload WHERE content_type_id=%s AND entity_id=%s '
        'ORDER BY create_user_id=%s DESC, ' + orderByClause + ' DESC LIMIT %s, %s',
        (contentTypeId, entityId, request.user.id if request.user.is_active else -1,
         EVENT_WALL_PHOTOS_PER_PAGE * (page_number - 1), EVENT_WALL_PHOTOS_PER_PAGE))
    )
    prefetch_votes(uploads=allEventPhotos, contentType=photoContentType, currentUser=auth.get_user(request) if request.user.is_active else None)
    prefetch_profile_name(uploads=allEventPhotos)
    return render(request, 'event/every-moment/wall.html',
                  {'event_photos': allEventPhotos, 'FB_APP_NAMESPACE': FB_APP_NAMESPACE, 'campaign': currentCampaign})


def attack_on_web(request):
    return render(request, 'event/attack-on-web/index.html')


def prizes(request):
    return render(request, 'event/attack-on-web/prizes.html')


def apply(request):
    return render(request, 'event/attack-on-web/apply.html')


def demo(request, app_name=None, app_id=None):
    appslist = DemoApp.objects.order_by('pk').all()
    app_dict = range(appslist.count())
    other_dict = range(int(appslist.count())-1)
    for i in range(appslist.count()):
        app_dict[i] = DemoApp.objects.get(pk=i+1)
        app_dict[i].en_title_fixed = app_dict[i].en_title.replace('-',' ')
        if i == 3:
            app_dict[i].en_title_fixed = 'Wake up!!!!'
    if not app_name:
        return render(request, 'event/attack-on-web/demo.html',{'applist':app_dict})
    if not app_id:
        return render(request, 'event/attack-on-web/demo.html',{'applist':app_dict})
    else:
        targetApp = DemoApp.objects.get(pk=app_id)
        otherApps = range(appslist.count()-1)
        if(app_name.lower() == targetApp.en_title.lower()):
            targetApp.ori_title = targetApp.en_title
            targetApp.en_title = targetApp.en_title.replace('-',' ')
            if int(app_id) == 4:
                 targetApp.en_title = u"Wake up!!!!"
            prevAppId = appslist.count() if int(app_id) == 1 else int(app_id)-1
            nextAppId = 1 if int(app_id) == appslist.count() else int(app_id)+1
            prevAppTitle = DemoApp.objects.get(pk=prevAppId).en_title
            nextAppTitle = DemoApp.objects.get(pk=nextAppId).en_title
            contentType = ContentType.objects.get(model='demoapp')
            prefetch_votes((targetApp, ), contentType, auth.get_user(request) if request.user.is_active else None)
            i = 0
            for j in range(appslist.count()):
                if j != (int(app_id)-1):
                    other_dict[i] = (DemoApp.objects.get(pk=j+1))
                    other_dict[i].en_title_fixed = DemoApp.objects.get(pk=j+1).en_title.replace('-',' ')
                    if j == 3:
                        other_dict[i].en_title_fixed = 'Wake up!!!!'
                    i = i + 1
                    #ther_dict.append(DemoApp.objects.get(1))
            return render(request, 'event/demo-app/index.html', {'thisApp':targetApp, 'voteCount': targetApp.vote_count,'prevAppId':prevAppId,'nextAppId':nextAppId,'prevAppTitle':prevAppTitle, 'nextAppTitle':nextAppTitle,'otherApps':other_dict})
        else:
            raise ObjectDoesNotExist


def microfilm(request):
    filmList = range(4)
    filmName = [u"謀智其中", u"火狐女孩爭奪戰", u"移動火狐，暢行無阻", u"夢想，從現在開始"]
    filmYid = ["qoWb2ngNe9k", "oUm9iKAkHlQ", "SbSiKqgcg3s", "Qt0uy4VVurk"]
    filmProducer = [];
    for film in filmList:
        n1 = random.randint(0, len(filmList)-1)
        n2 = random.randint(0, len(filmList)-1)
        tmp = filmList[n1]
        filmList[n1] = filmList[n2]
        filmList[n2] = tmp
        tmp = filmName[n1]
        filmName[n1] = filmName[n2]
        filmName[n2] = tmp
        tmp = filmYid[n1]
        filmYid[n1] = filmYid[n2]
        filmYid[n2] = tmp
    return render(request, 'event/attack-on-web/microfilm.html', {'filmList': filmList, 'filmName': filmName, 'filmYid':filmYid})


def microfilm_vote(request):
    filmList = range(4)
    filmName = [u"謀智其中", u"火狐女孩爭奪戰", u"移動火狐，暢行無阻", u"夢想，從現在開始"]
    filmYid = ["qoWb2ngNe9k", "oUm9iKAkHlQ", "SbSiKqgcg3s", "Qt0uy4VVurk"]
    filmProducer = []
    for film in filmList:
        n1 = random.randint(0, len(filmList)-1)
        n2 = random.randint(0, len(filmList)-1)
        tmp = filmList[n1]
        filmList[n1] = filmList[n2]
        filmList[n2] = tmp
        tmp = filmName[n1]
        filmName[n1] = filmName[n2]
        filmName[n2] = tmp
        tmp = filmYid[n1]
        filmYid[n1] = filmYid[n2]
        filmYid[n2] = tmp
    return render(request, 'event/microfilm-vote/index.html',  {'filmList': filmList, 'filmName': filmName, 'filmYid':filmYid})


def microfilm_vote_video(request, video_id):
    #filmName = [u"Firefox OS app 開發大賽－謀智其中", u"火狐女孩爭奪戰", u"移動火狐，暢行無阻", u"Firefox第二屆校園大使 東南區微電影"]
    #filmYid = ["QEDvKYUCD38", "oUm9iKAkHlQ", "SbSiKqgcg3s", "Qt0uy4VVurk"]
    video = Video.objects.get(pk=video_id)
    contentType = ContentType.objects.get(model='video')
    prefetch_votes((video, ), contentType, auth.get_user(request) if request.user.is_active else None)
    video_descriptions = [u"2013，台中。 因為一群身懷抱負、來自Mozilla組織的人們， 在這一如往常喧囂的城市當中，有甚麼正默默的醞釀著，且蓄勢待發…… 這個改變將帶來新希望，成為一股強勢的力量，翻轉人們的看法， 並徹底改寫網路世界的歷史…… Firefox OS—全新手機作業系統，與更美好的生活。", u"火狐女孩人見人愛，孰料竟遭邪惡的 Talking Tom 綁架，火狐先生要如何打破所有平台的屏障，成功搶救火狐女孩呢？", u"Firefox OS 的推出，行動作業的開放又向前跨了一大步。且看 Firefox OS 如何在各系統平台之間移動自如、暢行無阻。", u"夢想，是每個人生活的目標；希望，是讓人前進的動力。Firefox OS 提供的不單單只是手機，而是一個夢想及希望。"]
    return render(request, 'event/microfilm-vote/video.html',
                  {'filmName': video.title, 'filmYurl': video.url, 'filmId': video.id,
                   'voteCount': video.vote_count, 'voted': video.voted, 'imageId': str(int(video_id)-1),'description': video_descriptions[int(video_id)-1]})


def event_register(request, event_slug):
    currentEvent = Event.objects.get(slug=event_slug, status__in=('preparing', 'enrolling', 'enrolled'))
    currentUser = auth.get_user(request)
    data = {'event': currentEvent}
    if request.method == 'POST':
        if not request.user.is_authenticated():
            raise PermissionDenied
        is_update = Person.objects.filter(user=request.user).exists()
        if is_update:
            form = PersonForm(request.POST, instance=Person.objects.get(user=request.user))
        else:
            form = PersonForm(request.POST)
        data['form'] = form
        if form.is_valid():
            person = form.save(commit=False)
            if is_update:
                person.save()
            else:
                person.user = currentUser
                person.save()
            if not Participation.objects.filter(activity=currentEvent, participant=currentUser).exists():
                participation = Participation(activity=currentEvent, participant=currentUser, status='attend')
                participation.save()
            data['registered'] = True
    elif request.user.is_authenticated():
        if Person.objects.filter(user=currentUser).exists():
            data['form'] = PersonForm(instance=currentUser.get_profile())
        else:
            fbAuth = UserSocialAuth.objects.filter(user=currentUser, provider='facebook')
            initData = {}
            if fbAuth.exists():
                token = fbAuth.get().tokens['access_token']
                if token:
                    graph = facebook.GraphAPI(token)
                    me = graph.get_object('me', locale='zh_TW')
                    if 'name' in me:
                        initData['fullname'] = me['name']
                    if 'gender' in me and me['gender'] in genderMap.keys():
                        initData['gender'] = genderMap[me['gender']]
            data['form'] = PersonForm(initial=initData)
    return render(request, 'event/event_register.html', data)


def campaign_claim_award(request, campaign_slug, nav_template=None, award_name=None):
    print campaign_slug
    currentCampaign = Campaign.objects.get(slug=campaign_slug, status='result')
    awarded = None
    if request.user.is_active:
        currentUser = auth.get_user(request)
        if award_name:
            currentAwards = Award.objects.filter(~Q(price=None) & ~Q(price__name='sorry'), activity=currentCampaign,
                                                 winner=currentUser, name=award_name)
            if currentUser.email:
                unregCurrentAwards = Award.objects.filter(activity=currentCampaign, winner_extra=currentUser.email,
                                                          name=award_name)
            else:
                unregCurrentAwards = []
        else:
            currentAwards = Award.objects.filter(~Q(price=None) & ~Q(price__name='sorry'), activity=currentCampaign,
                                                 winner=currentUser)
            if currentUser.email:
                unregCurrentAwards = Award.objects.filter(activity=currentCampaign, winner_extra=currentUser.email)
            else:
                unregCurrentAwards = []
        awarded = currentAwards.exists() or unregCurrentAwards.exists()
    data = {'campaign': currentCampaign, 'awarded': awarded, 'nav_template': nav_template, 'MOCO_URL': MOCO_URL}
    if request.method == 'POST':
        if not request.user.is_authenticated():
            raise PermissionDenied
        is_update = Person.objects.filter(user=request.user).exists()
        if is_update:
            form = AwardClaimForm(request.POST, instance=Person.objects.filter(user=request.user).latest('user'))
        else:
            form = AwardClaimForm(request.POST)
        data['form'] = form
        if form.is_valid():
            person = form.save(commit=False)
            if is_update:
                person.save()
            else:
                person.user = currentUser
                person.save()
            for currentAward in currentAwards:
                currentAward.status = 'claimed'
                currentAward.save()
            for unregCurrentAward in unregCurrentAwards:
                unregCurrentAward.status = 'claimed'
                unregCurrentAward.winner = currentUser
                unregCurrentAward.save()
            if not Participation.objects.filter(Q(activity=currentCampaign) & Q(Q(participant=currentUser) | Q(note=currentUser.email))).exists():
                participation = Participation(activity=currentCampaign, participant=currentUser, status='attend')
                participation.save()
            data['registered'] = True
    elif request.user.is_active:
        profiles = Person.objects.filter(user=currentUser)
        if profiles.exists():
            data['form'] = AwardClaimForm(instance=profiles.latest('user'))
        else:
            fbAuth = UserSocialAuth.objects.filter(user=currentUser, provider='facebook')
            initData = {}
            if fbAuth.exists():
                token = fbAuth.latest('uid').tokens['access_token']
                if token:
                    graph = facebook.GraphAPI(token)
                    me = graph.get_object('me', locale='zh_TW')
                    if 'name' in me:
                        initData['fullname'] = me['name']
                    if 'gender' in me and me['gender'] in genderMap.keys():
                        initData['gender'] = genderMap[me['gender']]
            data['form'] = AwardClaimForm(initial=initData)
    return render(request, 'event/campaign_claim_award.html', data)


def lantern_festival(request, subpath=''):
    currentCampaign = Campaign.objects.get(slug=lanternFestivalCampaignSlug)
    return render(request, 'event/lantern-festival/index.html', {'campaign': currentCampaign})


def lantern_claim_code(request):
    currentCampaign = Campaign.objects.get(slug=lanternFestivalCampaignSlug)
    subscriber = request.GET['subscriber']
    existing = Award.objects.filter(name=u'產生認領碼', activity=currentCampaign, winner_extra=subscriber)
    claimCodes = Award.objects.filter(name=u'產生認領碼', activity=currentCampaign, status='waiting')
    if existing.exists():
        data = {'message': 'already.claimed', 'claim_code': existing[0].note}
    elif claimCodes.exists():
        if 1 == claimCodes.count():
            currentCampaign.status = 'end'
            currentCampaign.save()
        claimCode = claimCodes[0]
        claimCode.winner_extra = subscriber
        claimCode.status = 'awarded'
        claimCode.save()
        data = {'claim_code': claimCode.note}
    else:
        data = {'message': 'out.of.claim.code'}
    response = json.dumps(data)
    return HttpResponse(response, mimetype='application/json')


def chinese_valentines_day(request):
    currentCampaign = Campaign.objects.get(slug=chineseValentinesDayCampaignSlug)
    return render(request, 'event/chinese-valentines-day/index.html', {'campaign': currentCampaign})


def chinese_valentines_day_participate(request):
    currentCampaign = Campaign.objects.get(slug=chineseValentinesDayCampaignSlug)
    data = {}
    if request.method == 'POST':
        if 'running' == currentCampaign.status:
            email = request.POST['subscriber']
            if not Participation.objects.filter(activity=currentCampaign, note=email).exists():
                user = User.objects.get(pk=1)
                participation = Participation(activity=currentCampaign, participant=user, note=email, status='attend')
                participation.save()
                data['result'] = 'success'
            else:
                data['result'] = 'failed'
        else:
            data['result'] = 'failed'
    else:
        data['result'] = 'failed'

    response = json.dumps(data)
    return HttpResponse(response, mimetype='application/x-javascript')


def chinese_valentines_day_result(request):
    currentCampaign = Campaign.objects.get(slug=chineseValentinesDayCampaignSlug)
    if currentCampaign.status != 'result':
        return redirect('/campaign/chinese-valentines-day/')
    randomAwards = Award.objects.filter(name=u'隨機抽獎', activity=currentCampaign).order_by('order')
    return render(request, 'event/chinese-valentines-day/result.html',
                  {
                      'campaign': currentCampaign,
                      'randomAwards': randomAwards
                  })


@xframe_allow
@csrf_exempt
def review2014_login(request, template):
    return render(request, template)


@enable_jsonp
def review2014_quota(request):
    data = {'result': 'failed'}
    try:
        currentCampaign = Campaign.objects.get(slug=review2014CampaignSlug)
        price = Price.objects.get(name='redenvelope')
        awards = Award.objects.filter(name=u'贈獎', activity=currentCampaign, price=price,
                                          create_time__range=get_1day_range(datetime.now())).count()
        quota = min(price.quantity, 200 - awards)
        data['result'] = 'success'
        data['quota'] = quota
    except Exception as e:
        print e
    response = json.dumps(data)
    return HttpResponse(response, mimetype='application/x-javascript')


@enable_jsonp
def review2014_award(request):
    data = {'result': 'failed'}
    if request.user.is_active:
        currentCampaign = Campaign.objects.get(slug=review2014CampaignSlug)
        existing = Award.objects.filter(name=u'贈獎', activity=currentCampaign, winner=request.user)
        if currentCampaign.status == 'end':
            data['result'] = 'ended'
        elif not existing.exists() and 'score' in request.GET:
            price = Price.objects.get(name='redenvelope')
            # check total quota and daily quota
            quota = min(price.quantity,
                        200 - Award.objects.filter(name=u'贈獎', activity=currentCampaign, price=price,
                                                   create_time__range=get_1day_range(datetime.now())).count())
            if quota > 0:
                # save award, decrease price quantity
                price.quantity -= 1
                price.save()
                award = Award(name=u'贈獎', activity=currentCampaign, winner=request.user, price=price)
                award.save()

                data['slug'] = price.name
                data['name'] = price.description
                data['result'] = 'success'
                data['existing'] = False
            else:
                data['message'] = 'quota exceeded'
        elif existing.exists():
            data['result'] = 'success'
            data['slug'] = existing[0].price.name
            data['name'] = existing[0].price.description
            data['existing'] = True
        else:
            data['message'] = 'invalid request'
    else:
        data['message'] = 'unauthorized'
    response = json.dumps(data)
    return HttpResponse(response, mimetype='application/x-javascript')


@xframe_allow
@csrf_exempt
def firefox_family_award(request, template):
    return render(request, template)


@enable_jsonp
def firefox_family_get_ticket(request):
    periods = ('10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00',
               '15:30', '16:00', '16:30')
    weights = (4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3)
    day_mapping = {
        '1': '11/22',
        '2': '11/23',
    }
    data = {'result': 'failed'}
    if request.user.is_active:
        currentCampaign = Campaign.objects.get(slug=tenYearsCampaignSlug)
        existing = Award.objects.filter(name=u'早鳥票', activity=currentCampaign, winner=request.user)
        ticketExists = existing.exists()
        if currentCampaign.status == 'end':
            data['result'] = 'ended'
        elif not ticketExists and 'day' in request.GET:
            day = day_mapping[request.GET['day']]
            suggested_period = weighted_sample(periods, weights)[0]
            #save award
            session = '%s %s' % (day, suggested_period)
            while True:
                verification_code = generate_claim_code()
                if not Award.objects.filter(name=u'早鳥票', activity=currentCampaign, note=verification_code).exists():
                    break
            ticket = Award(name=u'早鳥票', activity=currentCampaign, note=verification_code,
                           winner=request.user, winner_extra=session)
            ticket.save()
            data['session'] = session
            data['code'] = verification_code
            data['result'] = 'success'
            data['existing'] = False
            generate_10years_ticket(data['session'], data['code'])
        elif ticketExists:
            data['result'] = 'success'
            data['session'] = existing[0].winner_extra
            data['code'] = existing[0].note
            data['existing'] = True
        else:
            data['message'] = 'invalid request'
    else:
        data['message'] = 'unauthorized'
    response = json.dumps(data)
    return HttpResponse(response, mimetype='application/x-javascript')


@enable_jsonp
def firefox_family_lottery(request):
    prices_levels = (('sorry', 'notebook', 'totebag', 'carsticker', 'nbsticker'),
                     ('mug', 'taipeipass', 'backpack', 'fxosphone'))
    data = {'result': 'failed'}
    if request.user.is_active:
        currentCampaign = Campaign.objects.get(slug=tenYearsCampaignSlug)
        existing = Award.objects.filter(name=u'幸運轉輪', activity=currentCampaign, winner=request.user)
        if currentCampaign.status == 'end':
            data['result'] = 'ended'
        elif not existing.exists() and 'level' in request.GET:
            level = int(request.GET['level'])
            price_keys = prices_levels[0] if level == 0 else prices_levels[0] + prices_levels[1]
            prices = Price.objects.filter(name__in=price_keys)
            weights = []
            for price in prices:
                if price.name == 'sorry':
                    weights += [1000, ]
                else:
                    weights += [price.quantity, ]
            winning_price = weighted_sample(prices, weights)[0]
            #save award, decrease price quantity
            if winning_price.name != 'sorry':
                winning_price.quantity -= 1
                winning_price.save()
            lottery_award = Award(name=u'幸運轉輪', activity=currentCampaign, winner=request.user, price=winning_price)
            lottery_award.save()
            data['slug'] = winning_price.name
            data['name'] = winning_price.description
            data['result'] = 'success'
            data['existing'] = False
        elif existing.exists():
            data['result'] = 'success'
            data['slug'] = existing[0].price.name
            data['name'] = existing[0].price.description
            data['existing'] = True
        else:
            data['message'] = 'invalid request'
    else:
        data['message'] = 'unauthorized'
    response = json.dumps(data)
    return HttpResponse(response, mimetype='application/x-javascript')


def firefox_day_verify(request, template):
    currentCampaign = Campaign.objects.get(slug=tenYearsCampaignSlug)
    code = request.GET['code'] if request.GET else None
    data = {}
    if code:
        award = Award.objects.filter(name=u'早鳥票', activity=currentCampaign, note=code)
        if award.exists():
            ticket = award[0]
            if ticket.status == 'waiting':
                ticket.status = 'claimed'
                ticket.save()
                data['result'] = 'success'
            else:
                data['result'] = 'claimed'
            if ticket.create_time > datetime(2014, 11, 11):
                data['type'] = 'normal'
            else:
                data['type'] = 'earlybird'
        else:
            data['result'] = 'failed'
    return render(request, template, data)


def list_recent_events(request):
    data = {}
    if request.method == 'GET' and 'secret' in request.GET and request.GET['secret'] == API_SECRET:
        events = Event.objects.filter(status='enrolling').order_by('-create_time')[:5]
        event_list = []
        for event in events:
            event_list += [{'title': event.title, 'date': event.start_time.strftime('%Y-%m-%d %H:%M:%S'), 'url': event.url}, ]
        data['result'] = 'success'
        data['events'] = event_list
    else:
        data['result'] = 'failed'
    response = json.dumps(data)
    return HttpResponse(response, mimetype='application/json')
