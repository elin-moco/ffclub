from django.contrib import admin
from django.contrib.admin import StackedInline
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *


class PersonInline(StackedInline):
    model = Person
    extra = 0


class CustomUserAdmin(UserAdmin):
    inlines = [PersonInline]

    def __init__(self, model, admin_site):
        super(CustomUserAdmin, self).__init__(model, admin_site)
        self.search_fields += ('person__fullname', 'person__address', 'person__occupation')
        self.list_filter += ('person__gender', 'person__status', 'person__subscribing')



admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# class PersonAdmin(ModelAdmin):
#     search_fields = ['fullname', 'address', 'occupation']
#     list_filter = ['gender', 'status', 'subscribing']
# admin.site.register(Person, PersonAdmin)
