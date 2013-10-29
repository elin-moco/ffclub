# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models


class Newsletter(models.Model):
    title = models.TextField(blank=False)
    issue = models.DateField(blank=False)
    volume = models.IntegerField(default=1)
    publish_date = models.DateField(default=datetime.now)

    def __unicode__(self):
        return unicode(self.issue + ': ' + self.title)

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
