from django.conf import settings
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # (r'^yoursite/', include('yoursite.foo.urls')),

	# (r'^admin/doc/', include('django.contrib.admindocs.urls')), 
	# And add 'django.contrib.admindocs' to INSTALLED_APPS
    (r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    )