from django.conf.urls.defaults import *

from appman.models import *

urlpatterns = patterns('appman.views',
	url(r'^applications/$', 'application_list', name="application-list"),
	url(r'^applications/add/$', 'application_add', name="application-add"),
	url(r'^applications/(?P<object_id>\d+)/$', 'application_detail', name="application-detail"),
	url(r'^applications/(?P<object_id>\d+)/edit/$', 'application_edit', name="application-edit"),
	url(r'^applications/(?P<object_id>\d+)/delete/$', 'application_delete', name="application-delete"),
	url(r'^applications/(?P<object_id>\d+)/remove/$', 'application_admin_remove', name="application-admin-remove"),
	url(r'^categories/$', 'category_list', name="category-list"),
	url(r'^categories/(?P<object_id>\d+)/edit/$', 'category_edit', name="category-edit"),
	url(r'^categories/add/$', 'category_add', name="category-add"),
	url(r'^categories/(?P<object_id>\d+)/remove/$', 'category_remove', name="category-remove")
)