from django.views.generic.list_detail import *
from django.views.generic.create_update import *

from appman.forms import *
from appman.models import *

def application_list(request):
	cs = Application.objects.all()
	return object_list(request, queryset=cs, template_object_name="application")
	
def application_form(request):
	return create_object(request, form_class=ApplicationForm, post_save_redirect="/app/list/")