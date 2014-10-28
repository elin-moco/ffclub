# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class ColorBundle(models.Model):
    bg_color = models.CharField(max_length=20, verbose_name='背景顏色')
    font_color = models.CharField(max_length=20, verbose_name='字體顏色')

    def __unicode__(self):
        return unicode('ColorBundle: ' + str(self.id) + ', BG: ' + self.bg_color + ', Font: ' + self.font_color)

    class Meta:
        verbose_name = verbose_name_plural = u'佈景主題色系'


class ThemeCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name='類別')
    description = models.CharField(max_length=2047, verbose_name='描述', blank=True)
    enabled = models.IntegerField(verbose_name='啟用', default=1)

    def __unicode__(self):
        return unicode('Category: ' + str(self.id) + ', ' + self.title)

    class Meta:
        verbose_name = verbose_name_plural = u'佈景主題類別'


class ThemeTemplate(models.Model):
    title = models.CharField(max_length=255, verbose_name='標題')
    description = models.CharField(max_length=2047, verbose_name='描述', blank=True)
    template_image = models.ImageField(upload_to=settings.TEMPLATE_THEME_FILE_PATH,
                                       max_length=255, db_index=True, verbose_name='圖片')
    icon_image = models.ImageField(upload_to=settings.TEMPLATE_THEME_FILE_PATH,
                                       max_length=255, db_index=True, verbose_name='縮圖')
    edit_image = models.ImageField(upload_to=settings.TEMPLATE_THEME_FILE_PATH,
                                       max_length=255, db_index=True, verbose_name='編輯圖')
    color = models.ForeignKey(ColorBundle)
    category = models.ForeignKey(ThemeCategory)
    used = models.IntegerField(verbose_name='使用次數', default=0)
    enabled = models.IntegerField(verbose_name='啟用', default=1)

    def __unicode__(self):
        return unicode('Template: ' + str(self.id) + ', ' + self.title)

    class Meta:
        verbose_name = verbose_name_plural = u'佈景主題樣板'


class UserTheme(models.Model):
    title = models.CharField(max_length=255, verbose_name='標題')
    description = models.CharField(max_length=2047, verbose_name='描述', blank=True)
    header_image = models.ImageField(upload_to=settings.USER_THEME_FILE_PATH,
                                     #width_field='image_large_width', height_field='image_large_height',
                                     max_length=255, db_index=True, verbose_name='圖片')
    icon_image = models.ImageField(upload_to=settings.USER_THEME_FILE_PATH,
                                   #width_field='image_large_width', height_field='image_large_height',
                                   max_length=255, db_index=True, verbose_name='縮圖')
    preview_image = models.ImageField(upload_to=settings.USER_THEME_FILE_PATH,
                                      #width_field='image_large_width', height_field='image_large_height',
                                      max_length=255, db_index=True, verbose_name='預覽圖')
    bg_color = models.CharField(max_length=20, verbose_name='背景顏色')
    font_color = models.CharField(max_length=20, verbose_name='字體顏色')
    template = models.ForeignKey(ThemeTemplate, null=True)
    category = models.ForeignKey(ThemeCategory, null=True)
    user = models.ForeignKey(User, null=True)
    enabled = models.IntegerField(verbose_name='啟用', default=0)
    covered = models.IntegerField(verbose_name='置頂', default=0)
    viewed = models.IntegerField(verbose_name='瀏覽次數', default=0)
    download = models.IntegerField(verbose_name='下載次數', default=0)
    likes = models.IntegerField(verbose_name='按讚次數', default=0)
    create_time = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return unicode('UserTheme: ' + str(self.id) + ', ' + self.title)

    class Meta:
        verbose_name = verbose_name_plural = u'自製佈景主題'