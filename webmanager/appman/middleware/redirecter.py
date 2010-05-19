from django.http import HttpResponseRedirect
from appman.utils.response import HttpRedirectException

class Redirecter(object):
    def process_exception(self, request, exception):
        if isinstance(exception, HttpRedirectException):
            return HttpResponseRedirect(exception.args[0])