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


csrf_protect_m = method_decorator(csrf_protect)


class ParticipationInline(TabularInline):
    model = Participation
    extra = 0


class AwardInline(TabularInline):
    model = Award
    extra = 0


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
        )
        return my_urls + urls

    @csrf_protect_m
    @transaction.commit_on_success
    def activity_award_prizes(self, request, object_id, extra_context=None):
        opts = self.model._meta
        app_label = opts.app_label

        obj = self.get_object(request, unquote(object_id))
        object_name = force_unicode(opts.verbose_name)
        if request.POST:
            obj_display = force_unicode(obj.title)
            self.message_user(request, u'%(name)s "%(obj)s" 已完成頒獎！' %
                                       {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj_display)})

        data = {
            'title': '頒獎典禮',
            "object_name": object_name,
            "object": obj,
            "opts": opts,
            "app_label": app_label,
        }
        return render(request, 'admin/activity_award_prizes.html', data)

    @csrf_protect_m
    @transaction.commit_on_success
    def activity_export_winners(self, request, object_id, extra_context=None):
        opts = self.model._meta
        app_label = opts.app_label

        obj = self.get_object(request, unquote(object_id))
        object_name = force_unicode(opts.verbose_name)
        if request.POST:
            obj_display = force_unicode(obj.title)
            self.message_user(request, u'已從 %(name)s "%(obj)s" 匯出得獎名單！' %
                                       {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj_display)})
        data = {
            'title': '匯出得獎名單',
            "object_name": object_name,
            "object": obj,
            "opts": opts,
            "app_label": app_label,
        }
        return render(request, 'admin/activity_export_winners.html', data)


class EventAdmin(ActivityAdmin):
    search_fields = ['title', 'description', 'location',
                     'orders__usage', 'orders__fullname', 'orders__email',
                     'orders__address', 'orders__occupation', 'orders__feedback']
    list_filter = ['num_of_ppl', 'create_time', 'status', 'orders__create_time', 'orders__status']
    inlines = [AwardInline, OrderInline, ParticipationInline, ImageUploadInline]


admin.site.register(Event, EventAdmin)


class CampaignAdmin(ActivityAdmin):
    search_fields = ['title', 'description']
    list_filter = ['create_time', 'status']
    inlines = [AwardInline, ParticipationInline, ImageUploadInline]


admin.site.register(Campaign, CampaignAdmin)


class VoteAdmin(ModelAdmin):
    search_fields = ['note']
    list_filter = ['vote_time', 'status']


admin.site.register(Vote, VoteAdmin)


class VideoAdmin(ModelAdmin):
    search_fields = ['title', 'description']
    list_filter = ['create_time', 'status']


admin.site.register(Video, VideoAdmin)
