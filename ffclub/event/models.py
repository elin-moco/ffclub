# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from django.db import models
from django.contrib.contenttypes import generic

from ffclub.upload.models import ImageUpload


class Activity(models.Model):
    title = models.CharField(max_length=255, verbose_name='活動名稱(*)')
    description = models.CharField(max_length=255, blank=True, default='')

    create_user = models.ForeignKey(User, related_name='hostedActivities')
    create_time = models.DateTimeField(default=datetime.now)
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(default=datetime.now)
    vote_time = models.DateTimeField(default=datetime.now)

    participants = models.ManyToManyField(User, related_name='activities', through='Participation')

    photos = generic.GenericRelation(ImageUpload)

    class Meta:
        verbose_name = verbose_name_plural = '活動'


class Event(Activity):

    location = models.CharField(max_length=255, blank=True, default='', verbose_name='舉辦地點')
    num_of_ppl = models.IntegerField(null=True, blank=True, verbose_name='預計人數')

    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    status = models.CharField(max_length=20,
                              choices=(('normal', '正常'), ('enrolling', '報名中'), ('shared', '已分享'), ('spam', '垃圾')),
                              default='normal')

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name = verbose_name_plural = '實體活動'


class Campaign(Activity):
    status = models.CharField(max_length=20,
                              choices=(('running', '進行中'), ('preparing', '準備中'), ('voting', '投票中'), ('end', '已結束')),
                              default='preparing')

    class Meta:
        verbose_name = verbose_name_plural = '線上活動'


class Participation(models.Model):
    note = models.CharField(max_length=255, blank=True, default='')
    participant = models.ForeignKey(User, related_name='+')
    activity = models.ForeignKey(Activity, related_name='+')
    status = models.CharField(max_length=20,
                              choices=(('attend', '參加'), ('decline', '拒絕'), ('maybe', '或許'), ('invited', '已邀請')),
                              default='invited')

    class Meta:
        verbose_name = verbose_name_plural = '活動參與'


class Vote(models.Model):
    note = models.CharField(max_length=255, blank=True, default='')
    voter = models.ForeignKey(User, related_name='+')
    vote_time = models.DateTimeField(default=datetime.now)

    content_type = models.ForeignKey(ContentType, related_name='votes')
    entity_id = models.PositiveIntegerField()
    entity_object = generic.GenericForeignKey('content_type', 'entity_id')

    status = models.CharField(max_length=20,
                              choices=(('approve', '贊成'), ('oppose', '反對'), ('neutral', '廢票')),
                              default='neutral')

    class Meta:
        verbose_name = verbose_name_plural = '活動投票'
