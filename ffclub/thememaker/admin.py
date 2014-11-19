from ffclub.base import admin
from django.contrib.admin import ModelAdmin
from .models import *


class ColorBundleAdmin(ModelAdmin):
    list_filter = ['bg_color', 'font_color']


class ThemeCategoryAdmin(ModelAdmin):
    search_fields = ['title', 'description']
    list_filter = ['enabled']


class ThemeTemplateAdmin(ModelAdmin):
    search_fields = ['title', 'description']
    list_filter = ['enabled', 'used', 'color', 'category']


class UserThemeAdmin(ModelAdmin):
    search_fields = ['title', 'description']
    list_filter = ['enabled', 'template', 'category', 'bg_color', 'font_color', 'covered',
                   'cc_type', 'viewed', 'download', 'likes']


admin.site.register(ColorBundle, ColorBundleAdmin)
admin.site.register(ThemeCategory, ThemeCategoryAdmin)
admin.site.register(ThemeTemplate, ThemeTemplateAdmin)
admin.site.register(UserTheme, UserThemeAdmin)
