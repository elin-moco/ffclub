# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied
from django.shortcuts import *
from django.contrib import auth
import commonware.log
import facebook
from social_auth.db.django_models import UserSocialAuth

from django.contrib.auth.models import User
from forms import PersonForm
from models import Person
from ffclub.settings import API_SECRET

log = commonware.log.getLogger('ffclub')
genderMap = {u'男性': 'male', u'女性': 'female'}


def register(request):
    """Main view."""
    if not request.user.is_authenticated():
        raise PermissionDenied
    if request.method == 'POST':
        is_update = Person.objects.filter(user=request.user).exists()
        if is_update:
            form = PersonForm(request.POST, instance=Person.objects.get(user=request.user))
        else:
            form = PersonForm(request.POST)
        data = {'form': form}
        if form.is_valid():
            person = form.save(commit=False)
            if is_update:
                person.save()
                return redirect('intro.home')
            else:
                person.user = auth.get_user(request)
                person.save()
                return redirect('user.register.complete')
    elif Person.objects.filter(user=request.user).exists():
        data = {'form': PersonForm(instance=request.user.get_profile())}
    else:
        fbAuth = UserSocialAuth.objects.filter(user=request.user, provider='facebook')
        initData = {}
        if fbAuth.exists():
            token = fbAuth.get().tokens['access_token']
            if token:
                graph = facebook.GraphAPI(token)
                me = graph.get_object('me', locale='zh_TW')
                if 'name' in me:
                    initData['fullname'] = me['name']
                if 'gender' in me and me['gender'] in genderMap.keys():
                    initData['gender'] = genderMap[me['gender']]

        data = {'form': PersonForm(initial=initData)}  # You'd add data here that you're sending to the template.

    return render(request, 'person/register.html', data)


def register_complete(request):
    """Main view."""
    data = {}  # You'd add data here that you're sending to the template.

    return render(request, 'person/register_complete.html', data)


def registered_user_count(request, provider=None):
    if 'secret' in request.GET and request.GET['secret'] == API_SECRET:
        if provider == 'facebook':
            count = UserSocialAuth.objects.filter(provider='facebook').count()
        else:
            count = User.objects.filter(is_active=True).count()
    else:
        raise PermissionDenied
    return HttpResponse(str(count), content_type='application/json')