import logging

from django.shortcuts import render
from django.forms.models import modelform_factory

import commonware
# from commonware import log
from funfactory.log import log_cef
from session_csrf import anonymous_csrf

from ffclub.event.models import Event


log = commonware.log.getLogger('ffclub')

def wall(request, template=None):
    """Main view."""
    data = {'form': modelform_factory(Event)()}  # You'd add data here that you're sending to the template.
    log.debug(template)
    return render(request, 'event/wall.html', data)
