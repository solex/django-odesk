from django.conf import settings
from odesk import Client

class DefaultClient(Client):

    def __init__(self, api_token=None):
        public_key = getattr(settings, 'ODESK_PUBLIC_KEY', None)
        secret_key = getattr(settings, 'ODESK_PRIVATE_KEY', None)
        if not (public_key and secret_key):
            raise ImproperlyConfigured(
                "The django_odesk.auth.AutoClientMiddleware requires "+\
                "both ODESK_PUBLIC_KEY and ODESK_PRIVATE_KEY "+\
                "settings to be specified.")
        super(DefaultClient, self).__init__(public_key, secret_key, api_token) 

class RequestClient(DefaultClient):

    def __init__(self, request):
        api_token = request.session.get('odesk_api_token', None) 
        super(RequestClient, self).__init__(api_token) 
    
