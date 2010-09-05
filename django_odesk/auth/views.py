from django.conf import settings
from django.http import HttpResponseRedirect

from django_odesk.core.clients import RequestClient
from django_odesk.auth import logout

def authenticate(request):
    logout(request)
    odesk_client = RequestClient(request)
    return HttpResponseRedirect(odesk_client.auth.auth_url())


def callback(request, redirect_url=None):
    odesk_client = RequestClient(request)
    frob = request.GET.get('frob', None)
    if frob:
        api_token, auth_user = odesk_client.auth.get_token(frob) 
        request.session['odesk_api_token'] = api_token
        request.session['odesk_auth_user_data'] = auth_user
        redirect_url = request.session.pop('odesk_redirect_url', redirect_url)
        if not redirect_url:
            redirect_url =  '/'   
        return HttpResponseRedirect(redirect_url)
    
    else:
        return HttpResponseRedirect(odesk_client.auth.auth_url())
    
