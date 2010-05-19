import os
from smtplib import SMTPException

from django.views.generic.list_detail import *
from django.views.generic.create_update import *
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.core.urlresolvers import reverse
from django.core.files import File 
from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.db.models import Q

from appman.forms import *
from appman.models import *
from appman.decorators import *
from appman.utils.fileutils import *
from appman.utils import get_contact_admin_email, reboot_os
from appman.utils.proj_connection import ProjectorsThread

# Helper

def render(request, template, opts = {}):
    return render_to_response(template, opts, context_instance=RequestContext(request))
    
#Non-Authenticated User Views
def home(request):
	return render(request,'appman/home.html')

#Authenticated User Views
@login_required
def contact(request):
    if request.method == 'POST':
        form = MessageToAdminForm(request.POST)
        if form.is_valid():
            subject = '[WallManager] Message from user %s' % request.user.email
            message = 'Dear WallManager administrator,\n\n\
                The user %s has sent you a message using the website\'s administrator contact form. The message is as follows:\n\n\
                %s' % (request.user.email, form.cleaned_data['message'])
            email_from = settings.DEFAULT_FROM_EMAIL
            email_to = get_contact_admin_email()
            try:
                send_mail(subject, message, email_from, [email_to])
                request.user.message_set.create(message="Your message was sent successfully to the designated contact administrator.")
            except SMTPException, e:
                request.user.message_set.create(message="Unable to send your message. Please try again later.")
    else:
        form = MessageToAdminForm()
    return render(request,'appman/contact.html',{'form': form})
    
@login_required
def application_list(request, scope='', object_id=False):
    cs = Application.objects.all()
    cat = ''
    if scope == 'mine':
        cs = cs.filter(owner = request.user)
    if object_id:
        try:
            cat = Category.objects.get(id = object_id)
            cs = cs.filter(category = cat)
        except Category.DoesNotExist:
            cat = ""
            
    return render(request,'appman/application_list.html', {
            'application_list': cs,
            'categories': Category.objects.all(),
            'cat': cat
        })

@login_required
def application_search(request):
    q = request.POST.get('q','')
    cs = Application.objects.filter(
            Q(name__icontains = q) |
            Q(description__contains = q) |
            Q(category__name__icontains = q) |
            Q(owner__first_name__icontains = q) |
            Q(owner__email__icontains = q)
        )
    return render(request,'appman/application_list.html', {
            'application_list': cs,
            'categories': Category.objects.all(),
            'query': q 
        })

@login_required
def application_log(request, object_id):
    cs = ApplicationLog.objects.filter(application = object_id)
    try:
        app = Application.objects.get(id=object_id)
    except Application.DoesNotExist:
        request.user.message_set.create(message="Invalid application's ID: %s."%object_id)
        return HttpResponseRedirect(reverse('application-list'))
        
    return render(request,'appman/application_log.html', {'logs': cs,'identifier':object_id, 'appname':app.name})

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
            request.user.message_set.create(message="Application successfully submitted." )
            return HttpResponseRedirect(reverse('application-detail', args=[str(app.id)]))
        else:
            request.user.message_set.create(message="Invalid form, please correct the following errors.")
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

def application_detail(request,object_id,form=ReportAbuseForm()):
    cs = Application.objects.all()
    try:
        app = Application.objects.get(id=object_id)
    except Application.DoesNotExist:
        request.user.message_set.create(message="Invalid application's ID: %s."%object_id)
        return HttpResponseRedirect(reverse('application-list'))
    return object_detail(request, extra_context={'form': form}, object_id=object_id, queryset=cs, template_object_name="application")

@staff_login_required
def application_admin_remove(request,object_id):
    """This function requires that the user is part of the staff"""

    try:
        app = Application.objects.get(id=object_id)
        request.user.message_set.create(message="Application %s removed successfully."%(app.name))
    except Application.DoesNotExist:
        request.user.message_set.create(message="Invalid application's ID: %s."%object_id)
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
            request.user.message_set.create(message="Invalid application's ID: %d."%object_id)
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
        request.user.message_set.create(message="Application %s deleted successfully."%app.name)
    except Application.DoesNotExist:
        request.user.message_set.create(message="Invalid application's ID: %d."%object_id)
        return HttpResponseRedirect(reverse('application-list'))
    app = get_object_or_404(Application, id=object_id)
    app.delete()
    return HttpResponseRedirect(reverse('application-list'))
    
@login_required    
def report_abuse(request, object_id):
    try:
        app = Application.objects.get(id=object_id)
        request.user.message_set.create(message="Application %s reported successfully."%app.name)
    except Application.DoesNotExist:
        request.user.message_set.create(message="Invalid application's ID: %d."%object_id)
        cs = Application.objects.all()
        return object_list(request, queryset=cs, template_object_name="application")
    app = get_object_or_404(Application, id=object_id)
    if request.method == 'POST':
        form = ReportAbuseForm(request.POST)
        if form.is_valid():
            abuse_description = form.cleaned_data['abuse_description']
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
        else:
            return application_detail(request, object_id, form)
        return HttpResponseRedirect(reverse('application-list'))
        
#Decorators
def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

def superuser_required(login_url=None):
    return user_passes_test(lambda u: u.is_superuser, login_url=login_url)
    
#Admin Views
@staff_required()
def projectors(request):
    if request.method == 'POST':
        form = ProjectorControlForm(request.POST)
        if form.is_valid():
            new_proj = form.save()
            thread = ProjectorsThread(new_proj)	
            thread.start()
            request.user.message_set.create(message="Projector settings will be modified. This operation may take up to 10 minutes.")
            return HttpResponseRedirect(reverse('projectors'))
    else:
        obj, flag = ProjectorControl.objects.get_or_create(id=1)
        form = ProjectorControlForm(instance=obj)
            
    return render(request,'appman/projectors.html', {'form': form})

@staff_required()
def screensaver(request):
    try:
        current_screensaver_time = ScreensaverControl.objects.get().screensaver_inactivity_time
    except ScreensaverControl.DoesNotExist:
        current_screensaver_time = ScreensaverControl.objects.create(screensaver_inactivity_time='15:00')
    
    if request.method == 'POST':
        form = ScreenSaverTimeForm(request.POST)
        if form.is_valid():
            time = form.cleaned_data['screensaver_time']
            if str(time) == "00:00:00":
                request.user.message_set.create(message="Time must be at least 00:01 (one minute).")
            else:
                ScreensaverControl.objects.create(screensaver_inactivity_time = time)
                request.user.message_set.create(message="Screensaver inactivity time was set successfully.")
    else:
        form = ScreenSaverTimeForm(data= {'screensaver_time': current_screensaver_time})
        
    return render(request,'appman/screensaver.html', {'current_screensaver_time': current_screensaver_time, 'form': form})

@superuser_required()
def manage_administrators(request):
    admins = User.objects.filter(is_staff = True)
    form_visible = False
    if request.method == 'POST':
        form = AddAdminForm(request.POST)
        if form.is_valid():
            try:
                new_admin = User.objects.get(email = form.cleaned_data['email'])
                new_admin.is_staff = True
                new_admin.is_superuser = (form.cleaned_data['type'] == 'Power')
                new_admin.save()  
                request.user.message_set.create(message="Administrator added.")
            except User.DoesNotExist:
                request.user.message_set.create(message="%s is not registered on the application." % email)
        else:
            form_visible = True
    else:
        form = AddAdminForm()
    return render(request,'appman/manage_admins.html', {
        'admins': admins,
        'form': form,
        'form_visible': form_visible,
    })

@superuser_required()
def remove_administrator(request, object_id):
    admin = get_object_or_404(User, id=object_id)
    admin.is_superuser = False
    admin.is_staff = False
    admin.save()
    request.user.message_set.create(message="Administrator removed.")
    return HttpResponseRedirect(reverse('manage-admins'))

@superuser_required()
def define_contact_admin(request):
    admin_list = User.objects.filter(is_staff = True)
    try:
        current_contact_admin = WallManager.objects.all()[0].contact
    except IndexError:
        current_contact_admin = None
    if request.method == 'POST':
        contact_admin = request.POST['contact_admin']
        WallManager.objects.create(contact = contact_admin)
        current_contact_admin = contact_admin
        request.user.message_set.create(message="The contact admin was defined successfully.")
    return render(request,'appman/define_contact_admin.html',{'admin_list': admin_list, 'current_contact_admin': current_contact_admin})

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
            request.user.message_set.create(message="Category %s added successfully."%cat.name)
            return HttpResponseRedirect(reverse('category-list'))
    else:
        form = form_class()

    return render(request,'appman/application_form.html', {
        'form': form,
    })

@staff_login_required
def category_edit(request, object_id):
    try:
        cat = Category.objects.get(id=object_id)
    except Category.DoesNotExist:
        request.user.message_set.create(message="Invalid category's ID: %s."%object_id)
        return HttpResponseRedirect(reverse('category-list'))
    return update_object(request, form_class=CategoryForm, 
            object_id=object_id, post_save_redirect=reverse('category-list'))

@staff_login_required
def category_remove(request, object_id):
    try:
        cat = Category.objects.get(id=object_id)
        request.user.message_set.create(message="Category %s removed successfully."%cat.name)
    except Category.DoesNotExist:
        request.user.message_set.create(message="Invalid category's ID: %s."%object_id)
        return HttpResponseRedirect(reverse('category-list'))
    cat = get_object_or_404(Category, id=object_id)
    cat.delete()
    return HttpResponseRedirect(reverse('category-list'))
    
@staff_login_required
def documentation_edit(request, documentation_id):
    return update_object(request, form_class=DocumentationForm, 
            object_id=documentation_id)
            
@staff_login_required
def documentation_menu(request):
    #shows the menu for selecting the documentation to edit
    cs = FlatPage.objects.all()
    return object_list(request, queryset=cs, template_object_name="flatpage")

@staff_login_required
def reboot(request):
    reboot_os()
    request.user.message_set.create(message="SenseWall will reboot shortly.")
    return HttpResponseRedirect(reverse('home'))
    
    