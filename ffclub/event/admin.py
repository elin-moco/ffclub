# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.encoding import force_unicode
from ffclub.base import admin
from django.contrib.admin import ModelAdmin, StackedInline, TabularInline
from django.contrib.admin.util import unquote
from .models import *
from ffclub.product.models import Order
from ffclub.upload.admin import ImageUploadInline
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from functools import update_wrapper
from django.db.models import Max, Count
import StringIO
import csv
from django.http import HttpResponse
from ffclub.event.utils import generate_claim_code
from django.core.exceptions import ValidationError

csrf_protect_m = method_decorator(csrf_protect)


class ParticipationInline(TabularInline):
    model = Participation
    extra = 0


# class AwardInline(TabularInline):
#     model = Award
#     extra = 0


class OrderInline(StackedInline):
    model = Order
    extra = 0


class ActivityAdmin(ModelAdmin):
    change_form_template = 'admin/custom_activity_change_form.html'

    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)
        urls = super(ActivityAdmin, self).get_urls()
        my_urls = patterns(
            '',
            url(r'^(?P<object_id>\d+)/award/$',
                wrap(self.activity_award_prizes),
                name='admin.activity.award.prizes'),
            url(r'^(?P<object_id>\d+)/export-winners/$',
                wrap(self.activity_export_winners),
                name='admin.activity.export.winners'),
            url(r'^(?P<object_id>\d+)/claim-award/$',
                wrap(self.activity_claim_award),
                name='admin.activity.claim.award'),
        )
        return my_urls + urls

    @csrf_protect_m
    @transaction.commit_on_success
    def activity_claim_award(self, request, object_id, extra_context=None):
        opts = self.model._meta
        app_label = opts.app_label
        obj = self.get_object(request, unquote(object_id))
        object_name = force_unicode(opts.verbose_name)
        error = None

        claimCodes = Award.objects.filter(name=u'產生認領碼', activity=obj).order_by('order')
        if request.POST:
            claim_code = request.POST['claim_code']
            claim = Award.objects.filter(name=u'產生認領碼', activity=obj, note=claim_code)
            if claim.exists():
                claim = claim[0]
                if claim.status != 'claimed':
                    claim.status = 'claimed'
                    claim.save()
                else:
                    error = '認領碼已使用過'
            else:
                error = '認領碼不正確'

        data = {
            'title': '輸入認領碼',
            'object_name': object_name,
            'object': obj,
            'opts': opts,
            'app_label': app_label,
            'error': error,
            'claim_codes': claimCodes,
        }
        return render(request, 'admin/activity_claim_award.html', data)


    @csrf_protect_m
    @transaction.commit_on_success
    def activity_award_prizes(self, request, object_id, extra_context=None):
        opts = self.model._meta
        app_label = opts.app_label

        obj = self.get_object(request, unquote(object_id))
        object_name = force_unicode(opts.verbose_name)
        participations = Participation.objects.filter(activity=obj).prefetch_related('participant', 'participant__person')
        participants = []
        anonymous_participants = []
        for participation in participations:
            if participation.note and not participation.note in anonymous_participants:
                anonymous_participants += [participation.note, ]
            elif not participation.participant in participants:
                participants += [participation.participant, ]
        uploads = ImageUpload.objects.filter(
            entity_id=obj.id,
            content_type=ContentType.objects.get_for_model(self.model)).prefetch_related('create_user', 'create_user__person').annotate(Count('votes')).order_by('-votes__count')
        uploaders = []
        uploadIds = []
        for upload in uploads:
            uploadIds += [upload.id, ]
            if not upload.create_user in uploaders:
                uploaders += [upload.create_user, ]
        votes = Vote.objects.filter(
            entity_id__in=uploadIds,
            content_type=ContentType.objects.get(model='imageupload')).prefetch_related('voter', 'voter__person')
        voters = []
        for vote in votes:
            if not vote.voter in voters:
                voters += [vote.voter, ]
        if request.POST:
            award_name = request.POST['award_name']
            #awarded_role = request.POST['awarded_role']
            winner_amount = int(request.POST['winner_amount'])
            #award_type = request.POST['award_type']
            repeat = request.POST['repeat']
            reaward = request.POST['reaward']
            obj_display = force_unicode(obj.title)
            if award_name == u'最高人氣獎':
                if reaward == 'yes':
                    Award.objects.filter(name=u'最高人氣獎', activity=obj).delete()
                    startIndex = 1
                else:
                    startIndex = Award.objects.filter(name=u'最高人氣獎', activity=obj).aggregate(Max('order'))['order__max'] + 1
                awardedWinners = Award.objects.filter(name=u'最高人氣獎', activity=obj).values('winner_id')
                awardedIds = [awardedWinner['winner_id'] for awardedWinner in awardedWinners]
                popUploaders = []
                for upload in uploads:
                    if upload.create_user.id not in awardedIds and upload.create_user not in popUploaders:
                        popUploaders += [upload.create_user, ]
                for index, uploader in enumerate(popUploaders):
                    if index == winner_amount:
                        break
                    award = Award(name=u'最高人氣獎', order=index+startIndex, winner=uploader, activity=obj)
                    award.save()
                self.message_user(request, u'已完成 %s 頒獎！' % award_name)
            elif award_name == u'投票幸運獎':
                if reaward == 'yes':
                    Award.objects.filter(name=u'投票幸運獎', activity=obj).delete()
                    startIndex = 1
                else:
                    startIndex = Award.objects.filter(name=u'投票幸運獎', activity=obj).aggregate(Max('order'))['order__max'] + 1
                if repeat == 'no':
                    awardedWinners = Award.objects.filter(activity=obj).values('winner_id')
                    awardedIds = [awardedWinner['winner_id'] for awardedWinner in awardedWinners]
                    filtered_voters = [voter for voter in voters if voter.id not in awardedIds]
                else:
                    filtered_voters = voters
                from random import shuffle
                shuffle(filtered_voters)
                for index, voter in enumerate(filtered_voters):
                    if index == winner_amount:
                        break
                    award = Award(name=u'投票幸運獎', order=index+startIndex, winner=voter, activity=obj)
                    award.save()
                self.message_user(request, u'已完成 %s 頒獎！' % award_name)
            elif award_name == u'隨機抽獎':
                if reaward == 'yes':
                    Award.objects.filter(name=u'隨機抽獎', activity=obj).delete()
                    startIndex = 1
                else:
                    startIndex = Award.objects.filter(name=u'隨機抽獎', activity=obj).aggregate(Max('order'))['order__max'] + 1
                if repeat == 'no':
                    awardedWinners = Award.objects.filter(activity=obj).values('winner_extra')
                    awardedIds = [awardedWinner['winner_extra'] for awardedWinner in awardedWinners]
                    filtered_participants = [participant for participant in anonymous_participants if participant not in awardedIds]
                else:
                    filtered_participants = anonymous_participants
                from random import shuffle
                shuffle(filtered_participants)
                user = User.objects.get(pk=1)
                for index, participant in enumerate(filtered_participants):
                    if index == winner_amount:
                        break
                    award = Award(name=u'隨機抽獎', order=index+startIndex, winner=user, winner_extra=participant, activity=obj)
                    award.save()
                self.message_user(request, u'已完成 %s 頒獎！' % award_name)
            elif award_name == u'產生認領碼':
                if reaward == 'yes':
                    Award.objects.filter(name=u'產生認領碼', activity=obj).delete()
                    startIndex = 1
                else:
                    startIndex = Award.objects.filter(name=u'產生認領碼', activity=obj).aggregate(Max('order'))['order__max'] + 1
                claim_codes = set()
                while len(claim_codes) <= (winner_amount - startIndex):
                    claim_codes.add(generate_claim_code())

                for claim_code in claim_codes:
                    award = Award(name=u'產生認領碼', winner=User.objects.get(pk=1), activity=obj, note=claim_code)
                    award.save()
                self.message_user(request, u'已完成 %s 頒獎！' % award_name)

            else:
                self.message_user(request, u'目前不支援此頒獎組合！請選擇正確的得獎角色和頒獎方式。')
        popularAwards = Award.objects.filter(name=u'最高人氣獎', activity=obj).prefetch_related('winner', 'winner__person').order_by('order')
        luckyAwards = Award.objects.filter(name=u'投票幸運獎', activity=obj).prefetch_related('winner', 'winner__person').order_by('order')
        claimCodes = Award.objects.filter(name=u'產生認領碼', activity=obj).order_by('order')
        randomAwards = Award.objects.filter(name=u'隨機抽獎', activity=obj).order_by('order')
        for claimCode in claimCodes:
            claimCode.no_profile = True
        data = {
            'title': '頒獎典禮',
            'object_name': object_name,
            'object': obj,
            'opts': opts,
            'app_label': app_label,
            'participants': participants,
            'anonymous_participants': anonymous_participants,
            'uploaders': uploaders,
            'voters': voters,
            'awards': {
                u'隨機抽獎': randomAwards,
                u'最高人氣獎': popularAwards,
                u'投票幸運獎': luckyAwards,
                u'產生認領碼': claimCodes,
            }
        }
        return render(request, 'admin/activity_award_prizes.html', data)

    def activity_export_winners(self, request, object_id, extra_context=None):
        obj = self.get_object(request, unquote(object_id))
        awards = Award.objects.filter(activity=obj).prefetch_related('winner', 'winner__person').order_by('name', 'order')
        output = StringIO.StringIO()
        writer = csv.writer(output)
        writer.writerow(['獎項', '順序', '姓名', '暱稱', 'Email', '電話', '地址', '註記', '狀態'])
        for award in awards:
            winner = award.winner
            if winner is None:
                row = [award.name.encode('utf-8'), ]
                row += [award.order, ]
                row += ['', ]
                row += ['', ]
                row += ['', ]
                row += ['', ]
                row += ['', ]
                row += [award.note, ]
                row += [award.status, ]
                writer.writerow(row)
            else:
                profile = winner.person if hasattr(winner, 'person') else None
                row = [award.name.encode('utf-8'), ]
                row += [award.order, ]
                row += [profile.fullname.encode('utf-8') if profile else '%s %s' % (winner.last_name.encode('utf-8'), winner.first_name.encode('utf-8')), ]
                row += [profile.nickname.encode('utf-8') if profile else '']
                row += [winner.email, ]
                row += [profile.phone if profile else '']
                row += [profile.address.encode('utf-8') if profile else '']
                row += [award.note, ]
                row += [award.status, ]
                writer.writerow(row)
        response = HttpResponse(output.getvalue(), mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s-campaign-awards.csv' % obj.slug
        return response


class EventAdmin(ActivityAdmin):
    search_fields = ['title', 'description', 'location',
                     'orders__usage', 'orders__fullname', 'orders__email',
                     'orders__address', 'orders__occupation', 'orders__feedback']
    list_filter = ['num_of_ppl', 'create_time', 'status', 'orders__create_time', 'orders__status']
    inlines = [OrderInline, ParticipationInline, ImageUploadInline]


admin.site.register(Event, EventAdmin)


class CampaignAdmin(ActivityAdmin):
    search_fields = ['title', 'description']
    list_filter = ['create_time', 'status']
    inlines = [ParticipationInline, ImageUploadInline]


admin.site.register(Campaign, CampaignAdmin)


class AwardAdmin(ModelAdmin):
    search_fields = ['name', 'note', 'winner_extra']
    list_filter = ['create_time', 'status', 'activity', 'price']

admin.site.register(Award, AwardAdmin)


class VoteAdmin(ModelAdmin):
    search_fields = ['note']
    list_filter = ['vote_time', 'status']


admin.site.register(Vote, VoteAdmin)


class PriceAdmin(ModelAdmin):
    search_fields = ['name', 'description']
    list_filter = ['quantity', 'status']

admin.site.register(Price, PriceAdmin)


class VideoAdmin(ModelAdmin):
    search_fields = ['title', 'description']
    list_filter = ['create_time', 'status']


admin.site.register(Video, VideoAdmin)


class DemoAppAdmin(ModelAdmin):
    search_fields = ['en_title', 'description']
    list_filter = ['create_time', 'status']


admin.site.register(DemoApp, DemoAppAdmin)
