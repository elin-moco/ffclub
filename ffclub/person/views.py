import logging

from django.shortcuts import *
from .forms import PersonForm
from django.core.urlresolvers import reverse
# from  django.contrib.auth.models import User
from django.contrib import auth

import commonware
# from commonware import log
from funfactory.log import log_cef
from session_csrf import anonymous_csrf

from ffclub.person.models import Person

log = commonware.log.getLogger('ffclub')


def register(request, template=None):
    """Main view."""
    if request.method == 'POST':
        form = PersonForm(request.POST)
        data = {'form': form}
        if form.is_valid():
            person = form.save(commit=False)
            person.user = auth.get_user(request)
            person.save()
            return HttpResponseRedirect(reverse('user.register.complete'))
    else:
        data = {'form': PersonForm()}  # You'd add data here that you're sending to the template.

    return render(request, 'person/register.html', data)


def register_complete(request, template=None):
    """Main view."""
    data = {}  # You'd add data here that you're sending to the template.
    log.debug(template)
    return render(request, 'person/register_complete.html', data)
