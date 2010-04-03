from django.conf.urls.defaults import *

from appman.models import *

urlpatterns = patterns('appman.views',
	(r'^app/list/$', 'application_list'),
)