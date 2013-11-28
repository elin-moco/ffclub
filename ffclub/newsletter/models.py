# -*- coding: utf-8 -*-

from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from ffclub import settings


class Newsletter(models.Model):
    title = models.TextField(blank=False)
    issue = models.DateField(blank=False)
    volume = models.IntegerField(default=1)
    publish_date = models.DateField(default=datetime.now)

    def __unicode__(self):
        return unicode(self.issue.strftime('%Y-%m-%d') + ': ' + self.title)

    class Meta:
        verbose_name = verbose_name_plural = u'電子報'
        db_table = u'issue'


class Subscription(models.Model):
    email = models.TextField(blank=False, db_column='u_email')
    status = models.IntegerField(default=1, db_column='u_status')
    edit_date = models.DateField(default=datetime.now)

    def __unicode__(self):
        return unicode(self.email + ':' + str(self.status))

    class Meta:
        verbose_name = verbose_name_plural = u'電子報訂閱'
        db_table = u'newsletter'


class Metadata(models.Model):
    name = models.CharField(max_length=255, blank=True, default='')
    type = models.CharField(max_length=20,
                            choices=(('number', '數字'), ('string', '字串'),
                                     ('datetime', '日期時間'), ('file', '檔案')),
                            default='string')
    index = models.PositiveIntegerField()

    create_user = models.ForeignKey(User, related_name='+')
    create_time = models.DateTimeField(default=datetime.now)

    issue = models.ForeignKey(Newsletter, related_name='metadata')

    def __unicode__(self):
        return unicode('%s = %s' % (self.name, self.value))

    class Meta:
        verbose_name = verbose_name_plural = '電子報擴充欄位'


class MetaString(Metadata):
    value = models.CharField(max_length=255, blank=True, default='', verbose_name='字串')


class MetaNumber(Metadata):
    value = models.FloatField(default=0.0, verbose_name='數字')


class MetaDatetime(Metadata):
    value = models.DateTimeField(default=datetime.now, verbose_name='時間')


class MetaFile(Metadata):
    value = models.FileField(upload_to=settings.FILE_PATH, max_length=255, db_index=True, verbose_name='檔案')
