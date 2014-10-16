# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from django.db import models
from django.contrib.contenttypes import generic

from ffclub.upload.models import ImageUpload


class Activity(models.Model):
    title = models.CharField(max_length=255, verbose_name='活動名稱(*)')
    description = models.CharField(max_length=255, blank=True, default='', verbose_name='活動說明')
    slug = models.CharField(max_length=255, unique=True, blank=True, default='', verbose_name='固定名稱',
                            help_text='用於網址和程式查詢，訂定後勿改動。')
    url = models.URLField(blank=True, default='', verbose_name='活動網址')

    create_user = models.ForeignKey(User, related_name='hostedActivities')
    create_time = models.DateTimeField(default=datetime.now)
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(default=datetime.now)
    vote_time = models.DateTimeField(default=datetime.now)

    participants = models.ManyToManyField(User, related_name='activities', through='Participation')

    photos = generic.GenericRelation(ImageUpload, content_type_field='content_type', object_id_field='entity_id')

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name = verbose_name_plural = '活動'


class Event(Activity):

    location = models.CharField(max_length=255, blank=True, default='', verbose_name='舉辦地點')
    num_of_ppl = models.IntegerField(null=True, blank=True, verbose_name='預計人數')

    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    status = models.CharField(max_length=20,
                              choices=(('preparing', '未開放'), ('enrolling', '報名中'), ('enrolled', '報名截止'),
                                       ('normal', '正常'), ('shared', '已分享'), ('spam', '垃圾')),
                              default='normal')

    def __unicode__(self):
        return unicode('%s: %s' % (self.title, self.status))

    class Meta:
        verbose_name = verbose_name_plural = '實體活動'


class Campaign(Activity):
    status = models.CharField(max_length=20,
                              choices=(('running', '進行中'), ('preparing', '準備中'), ('voting', '投票中'),
                                       ('end', '已結束'), ('result', '公佈結果')),
                              default='preparing')

    def __unicode__(self):
        return unicode('%s: %s' % (self.title, self.status))

    class Meta:
        verbose_name = verbose_name_plural = '線上活動'


class Participation(models.Model):
    note = models.CharField(max_length=255, blank=True, default='')
    participant = models.ForeignKey(User, related_name='+')
    activity = models.ForeignKey(Activity, related_name='+')
    status = models.CharField(max_length=20,
                              choices=(('attend', '參加'), ('decline', '拒絕'), ('maybe', '或許'), ('invited', '已邀請')),
                              default='invited')

    def __unicode__(self):
        return unicode('%s@%s: %s' % (self.participant.username, self.activity.title, self.status))

    class Meta:
        verbose_name = verbose_name_plural = '活動報名'


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

    def __unicode__(self):
        return unicode('%s + %s/%s: %s' % (self.voter.username, self.content_type, str(self.entity_id), self.status))

    class Meta:
        verbose_name = verbose_name_plural = '活動投票'


class Price(models.Model):
    name = models.CharField(max_length=255, blank=True, default='', verbose_name='獎品名稱',
                            help_text='用於網址和程式查詢，訂定後勿改動。')
    description = models.CharField(max_length=255, verbose_name='描述')
    quantity = models.IntegerField(verbose_name='數量')
    photos = generic.GenericRelation(ImageUpload, content_type_field='content_type', object_id_field='entity_id')
    status = models.CharField(max_length=20,
                              choices=(('normal', '正常'), ('lack', '庫存不足')),
                              default='normal')

    def __unicode__(self):
        return unicode('%s' % (self.name, ))

    class Meta:
        verbose_name = verbose_name_plural = '活動獎品'


class Award(models.Model):
    name = models.CharField(max_length=255, blank=True, default='', verbose_name='獎項名稱',
                            help_text='用於網址和程式查詢，訂定後勿改動。')
    order = models.IntegerField(default=0, verbose_name='得獎順位')
    note = models.CharField(max_length=255, blank=True, default='')
    winner = models.ForeignKey(User, related_name='+', verbose_name='得獎者', blank=True, null=True, default=None)
    winner_extra = models.CharField(max_length=255, blank=True, default='')
    price = models.ForeignKey(Price, related_name='+', blank=True, null=True, default=None)
    activity = models.ForeignKey(Activity, related_name='+')
    create_time = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=20,
                              choices=(('waiting', '待確認'), ('claimed', '已確認'), ('awarded', '已頒發')),
                              default='waiting')

    def __unicode__(self):
        return unicode('%s+%s@%s: %s' % (self.winner.username, self.name, self.activity.title, self.status))

    class Meta:
        verbose_name = verbose_name_plural = '活動頒獎'


class Video(models.Model):
    title = models.CharField(max_length=255, blank=True, default='')
    description = models.CharField(max_length=255, blank=True, default='')
    url = models.URLField()
    create_user = models.ForeignKey(User, related_name='+')
    create_time = models.DateTimeField(default=datetime.now)

    status = models.CharField(max_length=20,
                              choices=(('normal', '正常'), ('reported', '被檢舉'), ('spam', '垃圾')),
                              default='normal')

    def __unicode__(self):
        return unicode('%s: %s' % (self.title, self.status))

    class Meta:
        verbose_name = verbose_name_plural = '影片'


class DemoApp(models.Model):
    en_title = models.CharField(max_length=255, blank=True, default='')
    ch_title = models.CharField(max_length=255, blank=True, default='')
    description = models.CharField(max_length=255, blank=True, default='')
    marketplace_url = models.URLField(blank=True)
    create_user = models.ForeignKey(User, related_name='+')
    create_time = models.DateTimeField(default=datetime.now)

    status = models.CharField(max_length=20,
                              choices=(('normal', '正常'), ('reported', '被檢舉'), ('spam', '垃圾')),
                              default='normal')

    def __unicode__(self):
        return unicode('%s: %s' % (self.en_title, self.status))

    class Meta:
        verbose_name = verbose_name_plural = 'APP競賽'