import logging

from django.shortcuts import render

import commonware
# from commonware import log
from funfactory.log import log_cef
from session_csrf import anonymous_csrf


log = commonware.log.getLogger('ffclub')

def register(request, template=None):
    """Main view."""
    data = {}  # You'd add data here that you're sending to the template.
    log.debug(template)
    return render(request, 'person/register.html', data)

def register_complete(request, template=None):
    """Main view."""
    data = {}  # You'd add data here that you're sending to the template.
    log.debug(template)
    return render(request, 'person/register_complete.html', data)
