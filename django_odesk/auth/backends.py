try:
    import cPickle as pickle
except ImportError:
    import pickle
from urllib2 import HTTPError

from django.contrib.auth.backends import ModelBackend
from django_odesk.auth.models import get_user_model
from django_odesk.conf import settings
from django_odesk.core.clients import DefaultClient

class OdeskUser(object):

    # Django authentication system uses only `user_id` value to get
    # a User data from the backend. So we cannot acess the `request` to store
    # the data in the session. Asking odesk.com for user data on each request
    # is an obvious overkill.
    # So we have to use `user_id` value as a transport that carries
    # the user data between SimpleBackend and the AuthMiddleware.
    # This seems a bit crazy, but I could not find a better way

    @classmethod
    def get(cls, user_id):
        attrs = pickle.loads(user_id)
        return cls(**attrs)
    
    def __init__(self, username, first_name, last_name, email):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_active = True
        self.backend = (SimpleBackend.__module__, 'SimpleBackend') 

    def __unicode__(self):
        return self.username

    def __str__(self):
        return unicode(self).encode('utf-8')

    def save(self, *args, **kwargs):
        return None

    @property
    def id(self):
        attrs = {}
        for name in ['username', 'first_name', 'last_name', 'email']:
            attrs[name] = getattr(self, name)
        return pickle.dumps(attrs)

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

    

class SimpleBackend(object):

    def authenticate(self, token=None):
        client = DefaultClient(token)
        try:
            api_token, auth_user = client.auth.check_token()
        except HTTPError:
            return None

        username = auth_user['mail']
        first_name = auth_user['first_name']
        last_name = auth_user['last_name']
        email = auth_user['mail']
        user = OdeskUser(username, first_name, last_name,
                                       email)
        return user

    def get_user(self, user_id):
        return OdeskUser.get(user_id)

    def has_module_perms(self, user_obj, app_label):
        return True


class BaseModelBackend(ModelBackend):

    create_unknown_user = True

    def authenticate(self, token=None):
        client = DefaultClient(token)
        try:
            api_token, auth_user = client.auth.check_token()
        except HTTPError:
            return None

        user = None
        username = self.clean_username(auth_user)
        model = get_user_model()

        if self.create_unknown_user:
            user, created = model.objects.get_or_create(username=username)
            if created:
                user = self.configure_user(user, auth_user)
        else:
            try:
                user = model.objects.get(username=username)
            except model.DoesNotExist:
                pass
        return user

    def clean_username(self, auth_user):
        return auth_user['mail']

    def configure_user(self, user, auth_user):
        return user

    def get_user(self, user_id):
        model = get_user_model()
        try:
            return model.objects.get(pk=user_id)
        except model.DoesNotExist:
            return None


class ModelBackend(BaseModelBackend):

    @property
    def create_unknown_user(self):
        return settings.ODESK_CREATE_UNKNOWN_USER

    def configure_user(self, user, auth_user):
        user.first_name = auth_user['first_name']
        user.last_name = auth_user['last_name']
        user.email = auth_user['mail']
        admins = settings.ODESK_ADMINS
        superusers = settings.ODESK_SUPERUSERS
        if user.username in admins:
            user.is_staff = True
        if user.username in superusers:
            user.is_superuser = True
        user.set_unusable_password()
        user.save()
        return user


class TeamAuthBackend(ModelBackend):

    def authenticate(self, token=None):
        client = DefaultClient(token)
        try:
            api_token, auth_user = client.auth.check_token()
        except HTTPError:
            return None

        user = None
        username = self.clean_username(auth_user)
        model = get_user_model()
        
        userteams_refs = [team[u'reference'] for team in client.hr.get_teams()]
        
        for team in userteams_refs: 
            if int(team) in settings.ODESK_AUTH_TEAMS:
                if self.create_unknown_user:
                    user, created = model.objects.get_or_create(username=username)
                    if created:
                        user = self.configure_user(user, auth_user)
                else:
                    try:
                        user = model.objects.get(username=username)
                    except model.DoesNotExist:
                        pass
                return user
        return None

