import os

from django.views.generic.list_detail import *
from django.views.generic.create_update import *
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.core.urlresolvers import reverse
from django.core.files import File 
from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.flatpages.models import FlatPage

from appman.forms import *
from appman.models import *
from appman.decorators import *
from appman.utils.fileutils import *
from appman.utils import get_contact_admin_email

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
    form_class = ApplicationAddForm
    if request.method == 'POST':
        temporary_named_path = ""
        form = form_class(request.POST, request.FILES)
        if 'hidFileID' in request.POST and request.POST['hidFileID']:
            # If SWFUpload was used, hidFieldID is set to the filename
            uploaded_file = request.POST['hidFileID'].strip()
            
            # The file is saved on a temporary zip named user_ID.zip to prevent duplicates
            # Then we rename it to the real filename before saving to the database.
            
            user_unique_path = fullpath(get_filename_for_id(request.user.id), media_subfolder=settings.ZIP_TEMP_FOLDER)
            temporary_named_path = fullpath(get_unique_path(uploaded_file), media_subfolder=settings.ZIP_TEMP_FOLDER)

            if os.path.exists(user_unique_path):
                form.fields['zipfile'].required=False # allow form validation
                move_file(user_unique_path, temporary_named_path)
                
        if form.is_valid():
            app = form.save(commit=False)
            app.owner = request.user
            if temporary_named_path:
                app.zipfile = File(open("%s" % temporary_named_path))
                app.save()
                delete_path(temporary_named_path)
            else:
                app.save()
            return HttpResponseRedirect(reverse('application-detail', args=[str(app.id)]))
        else:
            if temporary_named_path:
                delete_path(temporary_named_path)
    else:
        form = form_class()
    return render(request,'appman/application_form.html', {
        'form': form,
    })

def application_upload(request):
    """ View that accepts SWFUpload uploads. Returns the filename of the saved file. """
    if request.method == 'POST' and request.GET and request.GET['user_id']:
        user_id = request.GET['user_id']
        user_unique_path = fullpath(get_filename_for_id(user_id), media_subfolder=settings.ZIP_TEMP_FOLDER)        
        delete_path(user_unique_path) # Delete previous files
        
        for field_name in request.FILES:
            uploaded_file = request.FILES[field_name]
            
            destination = open(user_unique_path, 'wb')
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
            destination.close()
            
            # indicate that everything is OK for SWFUpload
            return HttpResponse(uploaded_file.name, mimetype="text/plain")
        else:
            return HttpResponseBadRequest("A file is required for upload to work", mimetype="text/plain")
    else:
        return HttpResponseRedirect(reverse('application-add'))

def application_detail(request,object_id):
    cs = Application.objects.all()
    try:
        app = Application.objects.get(id=object_id)
    except Application.DoesNotExist:
        #TODO send message
        return HttpResponseRedirect(reverse('application-list'))
    return object_detail(request, extra_context={'form': ReportAbuseForm()}, object_id=object_id, queryset=cs, template_object_name="application")

@staff_login_required
def application_admin_remove(request,object_id):
    """This function requires that the user is part of the staff"""

    try:
        app = Application.objects.get(id=object_id)
    except Application.DoesNotExist:
        #TODO send message
        return HttpResponseRedirect(reverse('application-list'))
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
        try:
            app = Application.objects.get(id=object_id)
        except Application.DoesNotExist:
            #TODO send message
            return HttpResponseRedirect(reverse('application-list'))

        if filepath and os.path.isfile(filepath):
            app.zipfile = File(open(filepath))
            app.save()
    return update_object(request, form_class=ApplicationEditForm, 
            object_id=object_id, post_save_redirect=reverse('application-detail', args=[str(object_id)]))
            
@login_required
def application_delete(request, object_id):
    try:
        app = Application.objects.get(id=object_id)
    except Application.DoesNotExist:
        #TODO send message
        return HttpResponseRedirect(reverse('application-list'))
    app = get_object_or_404(Application, id=object_id)
    app.delete()
    return HttpResponseRedirect(reverse('application-list'))
    
@login_required    
def report_abuse(request, object_id):
    try:
        app = Application.objects.get(id=object_id)
    except Application.DoesNotExist:
        #TODO send message
        cs = Application.objects.all()
        return object_list(request, queryset=cs, template_object_name="application")
    app = get_object_or_404(Application, id=object_id)
    if request.method == 'POST':
        abuse_description = request.POST['abuse_description']
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = get_contact_admin_email()
        current_site = Site.objects.get_current()
        message = """ User %s reported an abuse in application %s (http://%s%s) described as: 
        
        %s """ % (request.user.email.strip(), app.name, current_site.domain, app.get_absolute_url(), abuse_description) 

        try:
            send_mail('[WallManager] Application ' + app.name + ' received an abuse report.', message, email_from, [email_to])
            request.user.message_set.create(message="Your report was sent successfully.")
        except:
            request.user.message_set.create(message="Failure while sending e-mail message containing the report. Please try again later.")
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
    return render(request,'appman/contact_admin.html')

@staff_login_required
def category_list(request):
    cs = Category.objects.all()
    return object_list(request, queryset=cs, template_object_name="category", 
        extra_context={'DEFAULT_CATEGORY': settings.DEFAULT_CATEGORY})

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
    try:
        cat = Category.objects.get(id=object_id)
    except Category.DoesNotExist:
        #TODO send message
        return HttpResponseRedirect(reverse('category-list'))
    return update_object(request, form_class=CategoryForm, 
            object_id=object_id, post_save_redirect=reverse('category-list'))

@staff_login_required
def category_remove(request, object_id):
    try:
        cat = Category.objects.get(id=object_id)
    except Category.DoesNotExist:
        #TODO send message
        return HttpResponseRedirect(reverse('category-list'))
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
    
@staff_login_required
def documentation_edit(request, documentation_id):
    return update_object(request, form_class=DocumentationForm, 
            object_id=documentation_id)
            
@staff_login_required
def documentation_menu(request):
    #shows the menu for selecting the documentation to edit
    cs = FlatPage.objects.all()
    return object_list(request, queryset=cs, template_object_name="flatpage")
