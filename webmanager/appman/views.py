from django.views.generic.list_detail import *
from django.views.generic.create_update import *
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from appman.forms import *
from appman.models import *
from appman.decorators import *

# Helper
def render(request, template, opts = {}):
    return render_to_response(template, opts, context_instance=RequestContext(request))
    
#Non-Authenticated User Views
def home(request):
	return render(request,'appman/home.html')
	
def documentation(request):
	return render(request,'appman/doc.html')

def faq(request):
	return render(request,'appman/faq.html')

#Authenticated User Views
@login_required
def contact(request):
    return render(request,'appman/contact.html')
    
@login_required
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
            return HttpResponseRedirect(reverse('application-detail', args=[str(app.id)]))
    else:
        form = form_class()
    return render(request,'appman/application_form.html', {'form': form,})
	
def application_detail(request,object_id):
    cs = Application.objects.all()
    return object_detail(request, object_id=object_id, queryset=cs, template_object_name="application")

@staff_login_required
def application_admin_remove(request,object_id):
    """This function requires that the user is part of the staff"""
    #TODO SEND EMAIL
    return application_delete(request, object_id)
    

@login_required
def application_edit(request, object_id):
    return update_object(request, form_class=ApplicationEditForm, 
            object_id=object_id, post_save_redirect=reverse('application-detail', args=[str(object_id)]))
            
@login_required
def application_delete(request, object_id):
    app = get_object_or_404(Application, id=object_id)
    app.delete()
    return HttpResponseRedirect("/app/list/")

#Decorators
def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

def superuser_required(login_url=None):
    return user_passes_test(lambda u: u.is_superuser, login_url=login_url)
    
#Admin Views
@staff_required()
def projectors(request):
    return render(request,'appman/projectors.html')

@staff_required()
def screensaver(request):
    return render(request,'appman/screensaver.html')

@staff_required()
def suspension(request):
    return render(request,'appman/suspension.html')

@staff_required()
def categories(request):
    return render(request,'appman/categories.html')

@superuser_required()
def manage_admins(request):
    return render(request,'appman/admins.html')

@superuser_required()
def contact_admin(request):
    return render(request,'appman/contact_admin.html')