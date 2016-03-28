import sys
import threading
from django.conf import settings
from django.core import urlresolvers
from django.http import Http404, HttpResponseServerError
from .debug import send_exception_email

try:
    import ipdb as pdb
except ImportError:
    import pdb

dbgconf = dict({
    'force_handle_500':     False,
    'debug_middleware':     False,
    'send_500_email_async': False,
}, **getattr(settings, 'DBGUTILS', {}))


#===============================================================================
class DebugRequestMiddleware(object):
    
    #---------------------------------------------------------------------------
    def process_request(self, request):
        if settings.DEBUG and dbgconf['debug_middleware']:
            pdb.set_trace()


#-------------------------------------------------------------------------------
def send_500_email(**kwargs):
    if dbgconf['send_500_email_async']:
        threading.Thread(target=send_exception_email, kwargs=kwargs).start()
    else:
        send_exception_email(**kwargs)


#===============================================================================
class ErrorMiddleware(object):

    #---------------------------------------------------------------------------
    @staticmethod
    def resolver():
        urlconf = settings.ROOT_URLCONF
        urlresolvers.set_urlconf(urlconf)
        return urlresolvers.RegexURLResolver(r'^/', urlconf)
    
    #---------------------------------------------------------------------------
    def process_exception(self, request, exception):
        # Get the exception info now, in case another exception is thrown later.
        if isinstance(exception, Http404):
            return
            
        if settings.DEBUG and not dbgconf['force_handle_500']:
            return
        
        return self.handle_500(request, exception)
        
    #---------------------------------------------------------------------------
    def handle_500(self, request, exception):
        exc_info = sys.exc_info()
        subject = 'Critical Error: {}'.format(
            getattr(request, 'path_info', '(path info unavaible)')
        )
        
        if hasattr(request, 'user') and request.user.is_authenticated():
            extra_info = 'User %s (%s):\n\n' % (request.user.username, request.user.email)
        else:
            extra_info = ''

        send_500_email(
            request=request,
            subject=subject, 
            exc_info=exc_info,
            extra_info=extra_info
        )
        
        resolver = self.resolver()
        if hasattr(resolver, 'resolve500'):
            callback, param_dict = resolver.resolve500()
        else:
            callback, param_dict = resolver.resolve_error_handler(500)
            
        return callback(request, **param_dict)
        

