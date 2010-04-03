from django.views.generic.list_detail import *

from appman.models import *

def application_list(request):
	cs = Application.objects.all()

	return object_list(request, **{ "queryset": cs, "template_object_name": "application" })