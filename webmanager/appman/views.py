from django.views.generic.list_detail import *
from django.views.generic.create_update import *
from django.shortcuts import render_to_response

from appman.forms import *
from appman.models import *

def application_list(request):
	cs = Application.objects.all()
	return object_list(request, queryset=cs, template_object_name="application")
	
def application_form(request):
	form_class = ApplicationForm
	if request.method == 'POST':
		form = form_class(request.POST, request.FILES)
		if form.is_valid():
			app = form.save(commit=False)
			
			try:
				app.owner = User.objects.get(email="teste@teste.com")
			except:
				app.owner = User.objects.create(email="teste@teste.com",level='U')
				
			app.save()
			return HttpResponseRedirect('/app/list/') # Redirect after POST
	else:
		form = form_class() # An unbound form

	return render_to_response('appman/application_form.html', {
		'form': form,
	})