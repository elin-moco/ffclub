# -*- coding: utf-8 -*-
from ffclub.base import admin
from django.contrib.admin import StackedInline, TabularInline
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from social_auth.db.django_models import UserSocialAuth
from .models import *


class UserSocialAuthInline(TabularInline):
    model = UserSocialAuth
    extra = 0
    verbose_name = verbose_name_plural = '社群網站認證'


class UserInline(StackedInline):
    model = User
    extra = 0


class PersonInline(StackedInline):
    model = Person
    extra = 0


class CustomUserAdmin(UserAdmin):
    inlines = [PersonInline, UserSocialAuthInline]

    def __init__(self, model, admin_site):
        super(CustomUserAdmin, self).__init__(model, admin_site)
        self.search_fields += ('person__fullname', 'person__address', 'person__occupation')
        self.list_filter += ('person__gender', 'person__status', 'person__subscribing')



#admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, GroupAdmin)

# class PersonAdmin(ModelAdmin):
#     search_fields = ['fullname', 'address', 'occupation']
#     list_filter = ['gender', 'status', 'subscribing']
# admin.site.register(Person, PersonAdmin)
