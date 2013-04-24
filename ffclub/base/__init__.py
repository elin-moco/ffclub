"""Application base, containing global templates."""
import re
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import redirect

old_ie_patterns = re.compile(".*MSIE [6-8]\.")


class BrowserDetectionMiddleware(object):
    def process_request(self, request):
        if old_ie_patterns.match(request.META['HTTP_USER_AGENT']):
            redirect_path = reverse('not.supported')
            if request.path != redirect_path:
                return HttpResponsePermanentRedirect(redirect_path)

