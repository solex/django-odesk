from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django_odesk.conf import settings

# DESIGN NOTE:
# We could do something like this in the default settings:
# ODESK_USER_MODEL = 'auth.User'
# But we need to be sure that we are using `django.contrib.auth.models.User`
# by default, which  might not be the case if there is another 'auth' app
# installed. That is why we use ODESK_CUSTOM_USER_MODEL, which is set to None
# by default

def get_user_model():
    custom_model = settings.ODESK_CUSTOM_USER_MODEL
    if not custom_model:
        return User
    app_label, model_name = custom_model.split('.')
    model = models.get_model(app_label, model_name)
    if model is None:
        raise ImproperlyConfigured('Unable to load the user model' +\
                    'check ODESK_CUSTOM_USER_MODEL in your project settings')
    return model
