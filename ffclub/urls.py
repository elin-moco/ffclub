from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
# from examples import urls

from funfactory.monkeypatches import patch
patch()

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
PROJECT_MODULE = 'ffclub'

urlpatterns = patterns('',
    # Example:
    (r'', include('%s.intro.urls' % PROJECT_MODULE)),
    (r'', include('%s.person.urls' % PROJECT_MODULE)),
    (r'', include('%s.event.urls' % PROJECT_MODULE)),
    (r'', include('%s.product.urls' % PROJECT_MODULE)),
    (r'^admin/', include(admin.site.urls)),
    # Generate a robots.txt
    (r'^robots\.txt$', 
        lambda r: HttpResponse(
            "User-agent: *\n%s: /" % 'Allow' if settings.ENGAGE_ROBOTS else 'Disallow' ,
            mimetype="text/plain"
        )
    )

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

## In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
