from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from django_odesk.core.clients import RequestClient

def login(request, template_name='registration/odesk_login.html'):
    return render_to_response(template_name, {}, 
            context_instance=RequestContext(request))

def authorize(request):
    if 'odesk_api_token' in request.session:
        del request.session['odesk_api_token']
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


def logout(request):
    request.session.flush()
    if hasattr(request, 'odesk_user'):
        request.odesk_user = AnonymousUser()
    return HttpResponseRedirect(reverse('django_odesk.auth.views.login'))
    
