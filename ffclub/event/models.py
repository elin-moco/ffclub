# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from ffclub.upload.models import ImageUpload


class Event(models.Model):

    title = models.CharField(max_length=255, verbose_name='活動名稱')
    description = models.CharField(max_length=255, blank=True, default='')
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(default=datetime.now)
    create_user = models.ForeignKey(User, related_name='events')
    create_time = models.DateTimeField(default=datetime.now)
    location = models.CharField(max_length=255, blank=True, default='', verbose_name='舉辦地點')
    num_of_ppl = models.IntegerField(null=True, verbose_name='預計人數')
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    photos = generic.GenericRelation(ImageUpload)
    status = models.CharField(max_length=20,
                              choices=(('normal', '正常'), ('spam', '垃圾')),
                              default='normal')

    def __unicode__(self):
        return unicode(self.title)
