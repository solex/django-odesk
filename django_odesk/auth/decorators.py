from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django_odesk.core.clients import RequestClient 

try:
    from functools import wraps
except ImportError: 
    def wraps(wrapped, assigned=('__module__', '__name__', '__doc__'),
              updated=('__dict__',)):
        def inner(wrapper):
            for attr in assigned:
                setattr(wrapper, attr, getattr(wrapped, attr))
            for attr in updated:
                getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
            return wrapper
        return inner

def auth_required(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if not RequestClient(request).auth.check_token():
            request.session['odesk_redirect_url'] = request.get_full_path()
            return HttpResponseRedirect(reverse('django_odesk.auth.views.login'))
        return function(request, *args, **kwargs)
    return wrapper
