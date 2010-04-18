"""This middleware takes the session identifier in a POST message and adds it to the cookies instead.

This is necessary because SWFUpload won't send proper cookies back; instead, all the cookies are
added to the form that gets POST-ed back to us.
"""

from django.conf import settings
from django.core.urlresolvers import reverse

class SWFUploadMiddleware(object):

    def process_request(self, request):
        if (request.method == 'POST') and (request.path == reverse('application-upload')) and \
                request.POST.has_key(settings.SESSION_COOKIE_NAME):
            request.COOKIES[settings.SESSION_COOKIE_NAME] = request.POST[settings.SESSION_COOKIE_NAME]
