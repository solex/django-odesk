from odesk import Client
from django.core.exceptions import ImproperlyConfigured
from django_odesk.conf import settings
from django_odesk.auth import ODESK_TOKEN_SESSION_KEY

class DefaultClient(Client):

    def __init__(self, api_token=None):
        public_key = settings.ODESK_PUBLIC_KEY
        secret_key = settings.ODESK_PRIVATE_KEY
        if not (public_key and secret_key):
            raise ImproperlyConfigured(
                "The django_odesk.core.clients.DefaultClient requires "+\
                "both ODESK_PUBLIC_KEY and ODESK_PRIVATE_KEY "+\
                "settings to be specified.")
        super(DefaultClient, self).__init__(public_key, secret_key, api_token) 

class RequestClient(DefaultClient):

    def __init__(self, request):
        api_token = request.session.get(ODESK_TOKEN_SESSION_KEY, None) 
        super(RequestClient, self).__init__(api_token) 
    
