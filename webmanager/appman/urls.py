from django.conf.urls.defaults import *

from appman.models import *

urlpatterns = patterns('appman.views',

	url(r'^$', 'home', name="home"),
	url(r'^doc/$', 'documentation', name="tech-doc"),
	url(r'^faq/$', 'faq', name="faq"),
	url(r'^contact/$', 'contact', name="contact-admin"),

	url(r'^applications/$', 'application_list', name="application-list"),
	url(r'^applications/add/$', 'application_add', name="application-add"),
	url(r'^applications/upload/$', 'application_upload', name="application-upload"),
	url(r'^applications/(?P<object_id>\d+)/$', 'application_detail', name="application-detail"),
	url(r'^applications/(?P<object_id>\d+)/edit/$', 'application_edit', name="application-edit"),
	url(r'^applications/(?P<object_id>\d+)/delete/$', 'application_delete', name="application-delete"),
	url(r'^applications/(?P<object_id>\d+)/remove/$', 'application_admin_remove', name="application-admin-remove"),
	url(r'^categories/$', 'category_list', name="category-list"),
	url(r'^categories/(?P<object_id>\d+)/edit/$', 'category_edit', name="category-edit"),
	url(r'^categories/add/$', 'category_add', name="category-add"),
	url(r'^categories/(?P<object_id>\d+)/remove/$', 'category_remove', name="category-remove"),
	
	url(r'^projectors/$', 'projectors', name="projectors"),
	url(r'^screensaver/$', 'screensaver', name="screensaver"),
	url(r'^suspension/$', 'suspension', name="suspension"),
	url(r'^documentation/edit/$','documentation_edit', name="documentation-edit"),
	
	url(r'^admins/$', 'manage_admins', name="manage-admins"),
	url(r'^admin_contact/$', 'contact_admin', name="define-admin"),
	url(r'^accounts/register/$', 'account_register', name = "account-register"),

)