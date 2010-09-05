try:
    from functools import update_wrapper, wraps
except ImportError:
    from django.utils.functional import update_wrapper, wraps  # Python 2.4 fallback.

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings


def auth_required(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if not request.odesk_user.is_authenticated():
            request.session['odesk_redirect_url'] = request.get_full_path()
            if request.session.get('odesk_api_token_renew', False):
                #If the user is logged-out because of forced token renewal,
                #don't send them to the login page
                login_url = reverse('django_odesk.auth.views.authenticate')
            else:
                login_url = getattr(settings, "ODESK_LOGIN_URL", 
                                    settings.LOGIN_URL) 
            return HttpResponseRedirect(login_url)
        return function(request, *args, **kwargs)
    return wrapper
