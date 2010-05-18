from django.conf import settings
from django.conf.urls.defaults import *

from django.contrib import admin
from appman.admin import EmailAdmin
admin.site = EmailAdmin()
admin.autodiscover()

urlpatterns = patterns('',

    (r'^admin/(.*)', admin.site.root),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'^', include('appman.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    )