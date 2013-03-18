import logging

from django.shortcuts import render

import commonware
# from commonware import log
from funfactory.log import log_cef
from session_csrf import anonymous_csrf


log = commonware.log.getLogger('ffclub')

def home(request, template=None):
    """Main view."""
    data = {}  # You'd add data here that you're sending to the template.
    log.debug(template)
    return render(request, 'intro/home.html', data)
