# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):

    user = models.OneToOneField(User, primary_key=True, unique=True)
    fullname = models.CharField(max_length=255, verbose_name='姓名(*)')
    gender = models.CharField(max_length=7, verbose_name='性別(*)',
                              choices=(('unknown', '未指定'), ('male', '男性'), ('female', '女性')), default='unknown')
    address = models.CharField(max_length=255, verbose_name='地址(*)')
    occupation = models.CharField(max_length=255, verbose_name='職業(*)')
    status = models.CharField(max_length=20,
                              choices=(('normal', '正常'), ('spam', '垃圾')),
                              default='normal')

    def __unicode__(self):
        return unicode(self.fullname)

# User.profile = property(lambda u: Person.objects.get_or_create(user=u)[0])