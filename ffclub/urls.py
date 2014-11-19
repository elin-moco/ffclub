from django.contrib.admin import autodiscover
from django.contrib.contenttypes.models import ContentType
from django.contrib.sitemaps import GenericSitemap
from django.http import HttpResponse
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import sitemaps
from django.views.generic.simple import redirect_to
from ffclub.base import ViewsSitemap, PathsSitemap
from ffclub.intro.views import login_redirect
from ffclub.settings import DEBUG, ENGAGE_ROBOTS
from commonware.response.decorators import xframe_allow

# from examples import urls

from funfactory.monkeypatches import patch
from ffclub.product.models import Product
from ffclub.upload.models import ImageUpload
from ffclub.base import admin
from django_browserid.views import Verify

patch()

autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
PROJECT_MODULE = 'ffclub'

product_dict = {
    'queryset': Product.objects.all(),
    'date_field': 'update_time'
}

event_photo_dict = {
    'queryset': ImageUpload.objects.filter(content_type=ContentType.objects.get(model='event')),
    'date_field': 'create_time'
}

sitemaps = {
    'base': ViewsSitemap(['intro.home', 'product.wall', 'event.wall', 'design.wall'], 0.8, 'monthly'),
    'base_minor': ViewsSitemap(['tos'], 0.3, 'yearly'),
    'products': GenericSitemap(product_dict, 0.7, 'monthly'),
    'event_photos': GenericSitemap(event_photo_dict, 0.6, 'weekly'),
    'campaign': PathsSitemap(
        ['/campaign/chinese-valentines-day/',
         '/campaign/lantern-festival/', '/campaign/every-moment/', '/events/attack-on-web/', '/events/microfilm-vote/'],
        0.5, 'monthly'),
}


urlpatterns = patterns(
    '',
    (r'', include('%s.base.urls' % PROJECT_MODULE)),
    (r'', include('%s.intro.urls' % PROJECT_MODULE)),
    (r'', include('%s.person.urls' % PROJECT_MODULE)),
    (r'', include('%s.event.urls' % PROJECT_MODULE)),
    (r'', include('%s.product.urls' % PROJECT_MODULE)),
    (r'', include('%s.newsletter.urls' % PROJECT_MODULE)),
    (r'', include('%s.thememaker.urls' % PROJECT_MODULE)),
    url(r'^login/redirect$', login_redirect, name='login.redirect'),
    url(r'^logout/?$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='intro.logout'),
    url(r'^browserid/browserid/verify/?$', xframe_allow(Verify.as_view()),
        name='browserid_verify'),
    # url(r'^browserid/', include('django_browserid.urls')),
    url(r'', include('social_auth.urls')),
    ('^media/uploads/(?P<path>.*)$', redirect_to, {'url': '/static/uploads/%(path)s'}),
    ('^media/share/(?P<path>.*)$', redirect_to, {'url': '/static/share/%(path)s'}),
    (r'^admin/', include(admin.site.urls)),
    # Generate a robots.txt
    (
        r'^robots\.txt$',
        lambda r: HttpResponse(
            "User-agent: *\n%s: /" % 'Allow' if ENGAGE_ROBOTS else 'Disallow',
            mimetype="text/plain"
        )
    ),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})


    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

## In DEBUG mode, serve media files through Django.
if DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns(
        '',
        (r'^media/img/sandstone/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media/img/sandstone/'}),
        (r'^media/img/tabzilla/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media/img/tabzilla/'})
    )
    urlpatterns += patterns(
        '',
        # url(r'^', include('debug_toolbar_htmltidy.urls')),
        url(r'', include('debug_toolbar_user_panel.urls')),
    )
