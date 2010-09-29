from urllib2 import HTTPError
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django_odesk.core.clients import RequestClient
from django_odesk.auth import ODESK_TOKEN_SESSION_KEY

class FakeManager(object):

    def add(self, *args, **kwargs):
        return None

    def create(self, *args, **kwargs):
        return None

    def get_or_create(self, *args, **kwargs):
        return None

    def remove(self, *args, **kwargs):
        return None

    def clear(self, *args, **kwargs):
        return None

class OdeskUser(object):

    def __init__(self, username, first_name, last_name, email):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_active = True
        self.message_set = FakeManager()

    def __unicode__(self):
        return self.username

    def __str__(self):
        return unicode(self).encode('utf-8')

    def save(self, *args, **kwargs):
        return None

    @property
    def id(self):
        return 1

    @property
    def pk(self):
        return 1

    @property
    def is_staff(self):
        admins = settings.ODESK_ADMINS
        return (self.username in admins)

    @property
    def is_superuser(self):
        superusers = settings.ODESK_SUPERUSERS
        return (self.username in superusers)

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_full_name(self):
        "Returns the first_name plus the last_name, with a space in between."
        full_name = u'%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def has_module_perms(self, *args, **kwargs):
        return self.is_superuser

    def has_perm(self, *args, **kwargs):
        return self.is_superuser

    def get_and_delete_messages(self):
        return []


def get_user(request):
    user = AnonymousUser()
    if ODESK_TOKEN_SESSION_KEY in request.session:
        client = RequestClient(request)
        try:
            api_token, auth_user = client.auth.check_token() 
            username = auth_user['mail']
            first_name = auth_user['first_name']
            last_name = auth_user['last_name']
            email = auth_user['mail']
            user = OdeskUser(username, first_name, last_name, 
                                           email)
        except HTTPError:
            pass
    return user


class LazyUser(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_user'):
            request._cached_user = get_user(request)
        return request._cached_user


class AuthenticationMiddleware(object):
    def process_request(self, request):
        request.__class__.user = LazyUser()
        return None
