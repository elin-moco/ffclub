"""Application base, containing global templates."""
import re
import datetime
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import redirect

old_ie_patterns = re.compile(".*MSIE [6-8]\.")


class ViewsSitemap(Sitemap):

    def __init__(self, pages=[], priority=None, changefreq=None):
        self.pages = pages
        self.changefreq = changefreq
        self.priority = priority

    def items(self):
        return self.pages

    def lastmod(self, item):
        # The day sitemap generated
        return datetime.datetime.now()

    def location(self, item):
        return reverse(item)


class BrowserDetectionMiddleware(object):
    def process_request(self, request):
        if old_ie_patterns.match(request.META['HTTP_USER_AGENT']):
            redirect_path = reverse('not.supported')
            if request.path != redirect_path:
                return HttpResponsePermanentRedirect(redirect_path)

