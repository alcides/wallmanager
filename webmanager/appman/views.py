import os

from django.views.generic.list_detail import *
from django.views.generic.create_update import *
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files import File 
from django.conf import settings

from appman.forms import *
from appman.models import *
from appman.decorators import *
from appman.utils.fileutils import *

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
        filepath = ""
        form = form_class(request.POST, request.FILES)
        if 'hidFileID' in request.POST:
            # If SWFUpload was used, hidFieldID is set to the filename
            filepath = fullpath(request.POST['hidFileID'].strip())
            if os.path.exists(filepath):
                form.fields['zipfile'].required=False
        if form.is_valid():
            app = form.save(commit=False)
            app.owner = request.user
            if filepath:
                app.zipfile = File(open("%s" % filepath))
            app.save()
            return HttpResponseRedirect(reverse('application-detail', args=[str(app.id)]))
    else:
        form = form_class()
    return render(request,'appman/application_form.html', {
        'form': form,
    })

def application_upload(request):
    """ View that accepts SWFUpload uploads. Returns the filename of the saved file. """
    if request.method == 'POST':
        for field_name in request.FILES:
            uploaded_file = request.FILES[field_name]
            
            destination_path = get_unique_path(uploaded_file.name)
            destination = open(fullpath(destination_path), 'wb+')
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
            destination.close()

        # indicate that everything is OK for SWFUpload
        return HttpResponse(destination_path, mimetype="text/plain")

    else:
        return HttpResponseRedirect(reverse('application-add'))

    
def application_detail(request,object_id):
    cs = Application.objects.all()
    return object_detail(request, object_id=object_id, queryset=cs, template_object_name="application")

@staff_login_required
def application_admin_remove(request,object_id):
    """This function requires that the user is part of the staff"""

    app = get_object_or_404(Application, pk=object_id)

    email_from = settings.DEFAULT_FROM_EMAIL
    email_to = app.owner.email
    message = 'Your application, ' + app.name + ', has been removed from the wallmanager by the staff for not respecting the Terms of Service.'
    send_mail('[WallManager] Application removed from the wall.', message, email_from, [email_to])

    return application_delete(request, object_id)


@login_required
def application_edit(request, object_id):
    if request.method == 'POST' and 'hidFileID' in request.POST:
        filepath = fullpath(request.POST['hidFileID'].strip())
        if filepath and os.path.isfile(filepath):
            app = Application.objects.get(id=object_id)
            app.zipfile = File(open(filepath))
            app.save()
    return update_object(request, form_class=ApplicationEditForm, 
            object_id=object_id, post_save_redirect=reverse('application-detail', args=[str(object_id)]))
            
@login_required
def application_delete(request, object_id):
    app = get_object_or_404(Application, id=object_id)
    app.delete()
    return HttpResponseRedirect(reverse('application-list'))

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

@superuser_required()
def manage_admins(request):
    return render(request,'appman/admins.html')

@superuser_required()
def contact_admin(request):
    admin_list = User.objects.filter(is_staff = True).exclude(is_superuser = True)
    try:
        current_contact_admin = WallManager.objects.all()[0].contact
    except IndexError:
        current_contact_admin = None
    if request.method == 'POST':
        contact_admin = request.POST['contact_admin']
        WallManager.objects.create(contact = contact_admin)
        current_contact_admin = contact_admin
        request.user.message_set.create(message="The contact admin was defined successfully.")
    return render(request,'appman/contact_admin.html',{'admin_list': admin_list, 'current_contact_admin': current_contact_admin})

@staff_login_required
def category_list(request):
    cs = Category.objects.all()
    return object_list(request, queryset=cs, template_object_name="category")

@staff_login_required
def category_add(request):
    form_class = CategoryForm
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.save()
            return HttpResponseRedirect(reverse('category-list'))
    else:
        form = form_class()

    return render_to_response('appman/category_form.html', {'form': form,})

@staff_login_required
def category_edit(request, object_id):
    return update_object(request, form_class=CategoryForm, 
            object_id=object_id, post_save_redirect=reverse('category-list'))

@staff_login_required
def category_remove(request, object_id):
    cat = get_object_or_404(Category, id=object_id)
    cat.delete()
    return HttpResponseRedirect(reverse('category-list'))

def account_register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/accounts/login/")

    return render_to_response("registration/register.html", {'form' : form })