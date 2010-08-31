from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ImproperlyConfigured

class OdeskUser(object):
    
    def __init__(self, username, first_name, last_name, email):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_active = True
        self.is_staff = False
        self.is_superuser = False

    def __unicode__(self):
        return self.username

    def __str__(self):
        return unicode(self).encode('utf-8')

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_full_name(self):
        "Returns the first_name plus the last_name, with a space in between."
        full_name = u'%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

class AuthenticationMiddleware(object):
    def process_request(self, request):
        if not hasattr(request, 'session'):
            raise ImproperlyConfigured(
                "The django-odesk authentication middleware requires "+\
                "session middleware to be installed. Edit your "+\
                "MIDDLEWARE_CLASSES setting to insert "+\
                "'django.contrib.sessions.middleware.SessionMiddleware'.")
        auth_user_data = request.session.get('odesk_auth_user_data', None)
        if auth_user_data:
            username = auth_user_data['mail']
            first_name = auth_user_data['first_name']
            last_name = auth_user_data['last_name']
            email = auth_user_data['mail']
            request.__class__.odesk_user = OdeskUser(username, first_name, 
                                                     last_name, email)
        else:
            request.__class__.odesk_user = AnonymousUser()
        return None
