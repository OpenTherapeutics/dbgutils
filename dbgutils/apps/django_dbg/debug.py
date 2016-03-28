import os
import sys
import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.handlers.wsgi import WSGIRequest
from django.views.debug import ExceptionReporter


#===============================================================================
class FakeEnviron(dict):
    
    #---------------------------------------------------------------------------
    def __missing__(self, *args, **kws):
        return 'N/A'


#-------------------------------------------------------------------------------
def fake_request():
    return WSGIRequest(FakeEnviron(os.environ,
        REQUEST_METHOD='Unknown',
        HTTP_HOST='http://example.com/'
    ))


#-------------------------------------------------------------------------------
def get_request_repr(request=None):
    try:
        return repr(request)
    except:
        return "Request repr() unavailable"


#-------------------------------------------------------------------------------
def exception_reporter(request=None, exc_info=None):
    exc_info = exc_info or sys.exc_info()
    request = request or fake_request()
    return ExceptionReporter(request, *exc_info)


#-------------------------------------------------------------------------------
def compose_and_send_debug_email(subject, body_text, body_html=None, fail_silently=True):
    recipients = [a[1] for a in settings.ADMINS]
    msg = EmailMessage(
        '{} {}'.format(settings.EMAIL_SUBJECT_PREFIX, subject),
        body_text,
        settings.SERVER_EMAIL,
        recipients
    )
    
    if body_html:
        msg.attach('500-traceback.html', body_html, 'text/html')

    try:
        return msg.send(fail_silently=fail_silently)
    except:
        logging.exception('Failed to deliver error email')
        return None


#-------------------------------------------------------------------------------
def send_exception_email(
    request=None,
    exc_info=None,
    extra_info='',
    subject=None
):
    request = request or fake_request()
    reporter = exception_reporter(request, exc_info or sys.exc_info())
    body_text = "{}{}\n\n{}\n\n".format(
        '{}\n'.format(extra_info) if extra_info else '',
        reporter.get_traceback_text(),
        get_request_repr(request)
    )
    return compose_and_send_debug_email(
        subject or '[EXCEPTION]: {}'.format(request.path),
        body_text,
        reporter.get_traceback_html(),
        False
    )

