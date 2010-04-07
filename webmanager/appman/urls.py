from django.conf.urls.defaults import *

from appman.models import *

urlpatterns = patterns('appman.views',
	(r'^app/list/$', 'application_list'),
	(r'^app/(?P<object_id>\d+)/$', 'application_detail'), 
	(r'^app/add/$', 'application_add'),
	(r'^app/edit/(?P<object_id>\d+)$', 'application_edit'),
	(r'^app/delete/(?P<object_id>\d+)$', 'application_delete'),
)