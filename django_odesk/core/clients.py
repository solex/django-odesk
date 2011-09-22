import logging

from odesk import Client
from django.core.exceptions import ImproperlyConfigured
from django_odesk.conf import settings
from django_odesk.auth import ODESK_TOKEN_SESSION_KEY, ENCRYPTION_KEY_NAME
from django_odesk.auth.encrypt import decrypt_token

try:
    ENCRYPT_API_TOKEN = settings.ENCRYPT_API_TOKEN
except AttributeError, e:
    ENCRYPT_API_TOKEN = False

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
        from_session = request.session.get(ODESK_TOKEN_SESSION_KEY, None)
        if ENCRYPT_API_TOKEN:
            encryption_key = request.COOKIES.get(ENCRYPTION_KEY_NAME, None)
            encrypted_token = from_session
            api_token = None
            if encryption_key and encrypted_token:
                api_token = decrypt_token(encryption_key, encrypted_token)
        else:
            api_token = from_session
        super(RequestClient, self).__init__(api_token) 
    
