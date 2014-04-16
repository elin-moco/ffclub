# -*- coding: utf-8 -*-
from django.views.decorators.cache import never_cache
from johnny import cache
from ffclub.settings import MOCO_URL, MYFF_URL
from ffclub.base import admin
from django.contrib.admin import ModelAdmin, TabularInline
from .models import *
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied, ValidationError
from django.forms.formsets import all_valid
from django.contrib.admin import widgets, helpers
from django.utils.encoding import force_text
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.admin.util import unquote, flatten_fieldsets, get_deleted_objects, model_format_dict
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils.html import escape, escapejs
import re
from django.contrib import auth
import os
from ffclub.newsletter.utils import build_meta_params

META_PATTERN = re.compile('^meta-(string|datetime|number|file)-([A-z][-A-z]*)(-([0-9]+))?$')

csrf_protect_m = method_decorator(csrf_protect)


class MetaStringInline(TabularInline):
    model = MetaString
    extra = 0


class MetaNumberInline(TabularInline):
    model = MetaNumber
    extra = 0


class MetaDatetimeInline(TabularInline):
    model = MetaDatetime
    extra = 0


class MetaFileInline(TabularInline):
    model = MetaFile
    extra = 0


def save_metadata(issue, values, files, all_metadata=None):

    items = list(values.items()) + list(files.items())
    sort_order = {}
    for key, value in items:
        if value and key.startswith('meta-') and key.endswith('-order'):
            name = key[5:-6]
            index_list = value.split(',')
            order = {}
            for i, index in enumerate(index_list):
                order[i+1] = int(index)
            sort_order[name] = order

    existing = {}

    if all_metadata:
        for meta in all_metadata:
            if meta.index == 0:
                existing[meta.name] = meta
            else:
                if meta.name not in existing:
                    existing[meta.name] = {}
                existing[meta.name][meta.index] = meta
                for order_key, order in sort_order.items():
                    if meta.name.startswith(order_key):
                        meta.index = order[meta.index]
                        meta.save()

    for key, value in items:
        meta_match = META_PATTERN.match(key)
        if meta_match and value:
            type = meta_match.group(1)
            name = meta_match.group(2)
            index = meta_match.group(4)
            if not index:
                index = 0

            metadata = None

            if name in existing:
                if index == 0:
                    metadata = existing[name]
                elif index in existing[name]:
                    metadata = existing[name][index]

            if index > 0:
                for order_key, order in sort_order.items():
                    if name.startswith(order_key):
                        index = order[index]
                        break

            if type == 'string':
                if metadata:
                    metadata.value = value
                else:
                    metadata = MetaString(name=name, type=type, index=index, value=value, issue=issue)
            elif type == 'number':
                if metadata:
                    metadata.value = float(value)
                else:
                    metadata = MetaNumber(name=name, type=type, index=index, value=float(value), issue=issue)
            elif type == 'datetime':
                if metadata:
                    metadata.value = datetime.strptime(value, '%Y-%m-%d')
                else:
                    metadata = MetaDatetime(name=name, type=type, index=index, issue=issue,
                                            value=datetime.strptime(value, '%Y-%m-%d'))
            elif type == 'file':
                if metadata:
                    metadata.value = value
                else:
                    metadata = MetaFile(name=name, type=type, index=index, value=value, issue=issue)

            if metadata:
                metadata.save()


class NewsletterAdmin(ModelAdmin):
    add_form_template = 'newsletter/custom_newsletter_form.html'
    change_form_template = 'newsletter/custom_newsletter_form.html'
    search_fields = ['title']
    list_filter = ['issue', 'volume', 'publish_date']
    inlines = [MetaStringInline, MetaNumberInline, MetaDatetimeInline, MetaFileInline, ]

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        for inline_class in self.inlines:
            inline = inline_class(self.model, self.admin_site)
            if request:
                if not (inline.has_add_permission(request) or
                        inline.has_change_permission(request, obj) or
                        inline.has_delete_permission(request, obj)):
                    continue
                if not inline.has_add_permission(request):
                    inline.max_num = 0
            inline_instances.append(inline)

        return inline_instances

    @csrf_protect_m
    @never_cache
    def changelist_view(self, request, extra_context=None):
        return super(NewsletterAdmin, self).changelist_view(request, extra_context)

    @csrf_protect_m
    @transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
        model = self.model
        opts = model._meta

        if not self.has_add_permission(request):
            raise PermissionDenied

        ModelForm = self.get_form(request)

        if request.method == 'POST':
            # currentUser = auth.get_user(request)
            form = ModelForm(request.POST, request.FILES)
            if form.is_valid():
                issue = form.save()
                save_metadata(issue, request.POST, request.FILES)

                post_url = reverse('admin:%s_%s_change' %
                                   (opts.app_label, opts.module_name),
                                   args=(issue.id, ),
                                   current_app=self.admin_site.name)
                return HttpResponseRedirect(post_url)

            else:
                print 'invalid'

        else:
            form = ModelForm()

        admin_form = helpers.AdminForm(form, list(self.get_fieldsets(request)),
            self.get_prepopulated_fields(request),
            self.get_readonly_fields(request),
            model_admin=self)

        params = build_meta_params(None, True)

        context = {
            'admin': True,
            'adminform': admin_form,
            'is_popup': "_popup" in request.REQUEST,
            'app_label': opts.app_label,
            'params': params,
            'NEWSLETTER_URL': 'http://'+MOCO_URL+'/newsletter/2014-01/',
            'MOCO_URL': MOCO_URL,
            'MYFF_URL': MYFF_URL,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, form_url=form_url, add=True)

    @csrf_protect_m
    @transaction.commit_on_success
    def change_view(self, request, object_id, form_url='', extra_context=None):
        model = self.model
        opts = model._meta

        obj = self.get_object(request, unquote(object_id))

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_text(opts.verbose_name), 'key': escape(object_id)})

        if request.method == 'POST' and "_saveasnew" in request.POST:
            return self.add_view(request, form_url=reverse('admin:%s_%s_add' % (opts.app_label, opts.module_name),
                                                           current_app=self.admin_site.name))

        ModelForm = self.get_form(request, obj)

        params = {
            'title': obj.title,
            'issue': obj.issue.strftime('%Y年%m月%d號').decode('utf-8'),
            'volume': obj.volume
        }

        all_metadata = list(MetaString.objects.filter(issue=obj)) + \
                       list(MetaDatetime.objects.filter(issue=obj)) + \
                       list(MetaNumber.objects.filter(issue=obj)) + \
                       list(MetaFile.objects.filter(issue=obj))

        if request.method == 'POST':
            # currentUser = auth.get_user(request)
            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                print 'valid'
                issue = form.save()

                save_metadata(issue, request.POST, request.FILES, all_metadata)

                all_metadata = list(MetaString.objects.filter(issue=obj)) + \
                               list(MetaDatetime.objects.filter(issue=obj)) + \
                               list(MetaNumber.objects.filter(issue=obj)) + \
                               list(MetaFile.objects.filter(issue=obj))

            else:
                print 'invalid'
        else:
            form = ModelForm(instance=obj)

        params = dict(params.items() + build_meta_params(all_metadata, True).items())

        admin_form = helpers.AdminForm(form, list(self.get_fieldsets(request, obj)),
            self.get_prepopulated_fields(request, obj),
            self.get_readonly_fields(request, obj),
            model_admin=self)


        context = {
            'admin': True,
            'adminform': admin_form,
            'is_popup': "_popup" in request.REQUEST,
            'app_label': opts.app_label,
            'params': params,
            'NEWSLETTER_URL': 'http://'+MOCO_URL+'/newsletter/2014-01/',
            'MOCO_URL': MOCO_URL,
            'MYFF_URL': MYFF_URL,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, form_url=form_url, add=True)

admin.site.register(Newsletter, NewsletterAdmin)


class SubscriptionAdmin(ModelAdmin):
    search_fields = ['email']
    list_filter = ['edit_date', 'status']

admin.site.register(Subscription, SubscriptionAdmin)


