from django.views.generic.list_detail import *
from django.views.generic.create_update import *
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from appman.forms import *
from appman.models import *
from appman.utils import log_file

def application_list(request):
	cs = Application.objects.all()
	return object_list(request, queryset=cs, template_object_name="application")
	
@login_required
def application_add(request):
    form_class = ApplicationForm
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.owner = request.user
            app.save()
            log_file.log_app_event(app, 'added')
            return HttpResponseRedirect(reverse('application-detail', args=[str(app.id)]))
    else:
        form = form_class()

    return render_to_response('appman/application_form.html', {
        'form': form,
    })
	
def application_detail(request,object_id):
	cs = Application.objects.all()
	return object_detail(request, object_id=object_id, queryset=cs, template_object_name="application")

@login_required
def application_edit(request, object_id):
    return update_object(request, form_class=ApplicationEditForm, 
            object_id=object_id, post_save_redirect=reverse('application-detail', args=[str(object_id)]))
            
@login_required
def application_delete(request, object_id):
    app = get_object_or_404(Application, id=object_id)
    app.delete()
    if (app is not Http404):
        log_file.log_app_event(app, 'deleted')
    return HttpResponseRedirect("/app/list/")

