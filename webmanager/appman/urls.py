from django.conf.urls.defaults import *

from appman.models import *

urlpatterns = patterns('appman.views',
	url(r'^app/list/$', 'application_list', name="application-list"),
	url(r'^app/add/$', 'application_add', name="application-add"),
	url(r'^app/(?P<object_id>\d+)/$', 'application_detail', name="application-detail"),
	url(r'^app/(?P<object_id>\d+)/edit/$', 'application_edit', name="application-edit"),
	url(r'^app/(?P<object_id>\d+)/delete/$', 'application_delete', name="application-delete"),
	url(r'^app/(?P<object_id>\d+)/remove/$', 'application_admin_remove', name="application-admin-remove"),
	url(r'^cat/list/$', 'category_list', name="category-list"),
	url(r'^cat/(?P<object_id>\d+)/edit/$', 'category_edit', name="category-edit"),
	url(r'^cat/add/$', 'category_add', name="category-add"),
	url(r'^cat/(?P<object_id>\d+)/remove/$', 'category_remove', name="category-remove")
)