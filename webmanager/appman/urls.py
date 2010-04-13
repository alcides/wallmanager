from django.conf.urls.defaults import *

from appman.models import *

urlpatterns = patterns('appman.views',
	url(r'^$', 'home', name="home"),
	url(r'^doc/$', 'documentation', name="tech-doc"),
	url(r'^faq/$', 'faq', name="faq"),
	url(r'^contact/$', 'contact', name="contact-admin"),
	url(r'^app/list/$', 'application_list', name="application-list"),
	url(r'^app/add/$', 'application_add', name="application-add"),
	url(r'^projectors/$', 'projectors', name="projectors"),
	url(r'^screensaver/$', 'screensaver', name="screensaver"),
	url(r'^suspension/$', 'suspension', name="suspension"),
	url(r'^categories/$', 'categories', name="categories"),
	url(r'^admins/$', 'manage_admins', name="manage-admins"),
	url(r'^admin_contact/$', 'contact_admin', name="define-admin"),
	url(r'^app/(?P<object_id>\d+)/$', 'application_detail', name="application-detail"),
	url(r'^app/(?P<object_id>\d+)/edit/$', 'application_edit', name="application-edit"),
	url(r'^app/(?P<object_id>\d+)/delete/$', 'application_delete', name="application-delete"),
	url(r'^app/(?P<object_id>\d+)/remove/$', 'application_admin_remove', name="application-admin-remove"),
)