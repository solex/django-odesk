from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django_odesk.core.clients import DefaultClient
from django_odesk.auth import ODESK_REDIRECT_SESSION_KEY, \
                              ODESK_TOKEN_SESSION_KEY

def authenticate(request):
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
    request.session[ODESK_REDIRECT_SESSION_KEY] = redirect_to
    odesk_client = DefaultClient()
    return HttpResponseRedirect(odesk_client.auth.auth_url())


def callback(request, redirect_url=None):
    odesk_client = DefaultClient()
    frob = request.GET.get('frob', None)
    if frob:
        token, auth_user = odesk_client.auth.get_token(frob)
        request.session[ODESK_TOKEN_SESSION_KEY] = token
        #TODO: Get rid of (conceptually correct) additional request to odesk.com
        user = django_authenticate(token = token)
        login(request, user)
        redirect_url = request.session.pop(ODESK_REDIRECT_SESSION_KEY, 
                                           redirect_url)
        if not redirect_url:
            redirect_url =  '/'   
        return HttpResponseRedirect(redirect_url)
    
    else:
        return HttpResponseRedirect(odesk_client.auth.auth_url())
    
