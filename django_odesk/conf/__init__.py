from django.conf import settings as django_settings
from django_odesk.conf import default_settings

class AppSettings(object):
    
    def __init__(self, django_settings, default_settings):
        self.django_settings = django_settings
        self.default_settings = default_settings

    def __getattr__(self, name):
        return getattr(self.django_settings, name,
                       getattr(self.default_settings, name))

settings = AppSettings(django_settings, default_settings)
