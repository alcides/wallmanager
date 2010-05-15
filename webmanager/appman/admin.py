from django import http
from django.contrib import admin
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy, ugettext as _
from django.views.decorators.cache import never_cache
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.sites import LOGIN_FORM_KEY, ERROR_MESSAGE

from appman.models import *

class EmailAdmin(AdminSite):
    def login(self, request):
        """ Login method without the email information. """
        if not request.POST.has_key(LOGIN_FORM_KEY):
            if request.POST:
                message = _("Please log in again, because your session has expired.")
            else:
                message = ""
            return self.display_login_form(request, message)

        # Check that the user accepts cookies.
        if not request.session.test_cookie_worked():
            message = _("Looks like your browser isn't configured to accept cookies. Please enable cookies, reload this page, and try again.")
            return self.display_login_form(request, message)
        else:
            request.session.delete_test_cookie()

        # Check the password.
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = auth.authenticate(username=username, password=password)
        if user is None:
            message = ERROR_MESSAGE
            return self.display_login_form(request, message)

        # The user data is correct; log in the user in and continue.
        else:
            if user.is_active and user.is_staff:
                auth.login(request, user)
                return http.HttpResponseRedirect(request.get_full_path())
            else:
                return self.display_login_form(request, ERROR_MESSAGE)
        #do_login = never_cache(do_login)

admin.site.register(Application)
admin.site.register(ApplicationLog)
admin.site.register(Category)
