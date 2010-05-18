from django.conf.urls.defaults import *

from appman.models import *

urlpatterns = patterns('appman.views',

	url(r'^$', 'home', name="home"),
	url(r'^contact/$', 'contact', name="contact-admin"),

	url(r'^applications/$', 'application_list', name="application-list"),
	url(r'^applications/add/$', 'application_add', name="application-add"),
	url(r'^applications/upload/$', 'application_upload', name="application-upload"),
	url(r'^applications/(?P<object_id>\d+)/$', 'application_detail', name="application-detail"),
	url(r'^applications/(?P<object_id>\d+)/edit/$', 'application_edit', name="application-edit"),
	url(r'^applications/(?P<object_id>\d+)/delete/$', 'application_delete', name="application-delete"),
	url(r'^applications/(?P<object_id>\d+)/log/$', 'application_log', name="application-log"),
	url(r'^applications/(?P<object_id>\d+)/remove/$', 'application_admin_remove', name="application-admin-remove"),
    url(r'^applications/(?P<object_id>\d+)/report_abuse/$', 'report_abuse', name="report-abuse"),
	url(r'^applications/search/$', 'application_search', name="application-search"),
	url(r'^applications/cat/(?P<object_id>\d+)/$', 'application_list', name="application-list"),
	url(r'^applications/(?P<scope>\w+)/$', 'application_list', name="application-list"),
	url(r'^categories/$', 'category_list', name="category-list"),
	url(r'^categories/(?P<object_id>\d+)/edit/$', 'category_edit', name="category-edit"),
	url(r'^categories/add/$', 'category_add', name="category-add"),
	url(r'^categories/(?P<object_id>\d+)/remove/$', 'category_remove', name="category-remove"),
	
	url(r'^reboot/$', 'reboot', name="reboot"),
	url(r'^projectors/$', 'projectors', name="projectors"),
	url(r'^screensaver/$', 'screensaver', name="screensaver"),
	url(r'^documentation/menu/$','documentation_menu', name="documentation-menu"),
	url(r'^documentation/(?P<documentation_id>\d+)/edit/$','documentation_edit', name="documentation-edit"),
	
	url(r'^admins/$', 'manage_admins', name="manage-admins"),
	url(r'^admins/contact/$', 'define_contact_admin', name="define-admin"),

)