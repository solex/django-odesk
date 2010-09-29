from django.contrib.auth.backends import ModelBackend
from django_odesk.auth.models import get_user_model
from django_odesk.conf import settings
from django_odesk.core.clients import DefaultClient

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
