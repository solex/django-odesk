============
Django oDesk
============

Requirements
------------

    * `python-odesk`

`django-odesk` uses Django session mechanism, so session middleware should 
be enabled.


Authentication
--------------

To make minimal use of authentication app, include `django_odesk.auth.urls`
to your `urls.py`::

    (r'^auth/', include('django_odesk.auth.urls')),

You will also need to set a pair of oDesk API keys in `settings.py`::
    
    ODESK_PUBLIC_KEY = '(your public key)'
    ODESK_PRIVATE_KEY = '(your private key)'

Then you may use the `auth_required` decorator to demand an oDesk 
authentication on your views::

    from django_odesk.auth.decorators import auth_required
    
    @auth_required
    def my_view(request):
        ...


This will make user authenticate with oDesk and store their data in the 
session.
You may also use a middleware that populates `request` with `odesk_user` 
attribute, which is a special object with an interface similar to 
`django.contrib.auth.User`. To enable it, include the 
`django_odesk.auth.middleware.Authentication` middleware to the list of
middleware classes::

    
    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        ...
        'django_odesk.auth.middleware.AuthenticationMiddleware',
    )

You may use `request.odesk_user` much in a way that you would use Django's 
User object::

    >>> request.odesk_user.username
    'solex@odesk.com'
    >>> request.odesk_user.first_name
    'Oleksiy'
    >>> request.odesk_user.is_authenticated()
    True

Default values for "security-related" attributes are::

    >>> request.odesk_user.is_active
    True
    >>> request.odesk_user.is_staff
    False
    >>> request.odesk_user.is_superuser
    False

It is up to you to change them.
If the user is not authenticated, `request.odesk_user` is
`django.contrib.auth.models.AnonymousUser`.

