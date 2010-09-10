============
Django oDesk
============

Requirements
============

    * `python-odesk`


Authentication
==============


Quick start
-----------

Before you may use oDesk APIs, you will need to obtain your pair of API keys.
Visit the `oDesk API Center documentation <http://developers.odesk.com/Authentication#authentication>`_
for full details.

Include `django_odesk.auth.urls` to your `urls.py`::

    (r'^odesk_auth/', include('django_odesk.auth.urls')),

Use an URL of `django_odesk.auth.views.callback` as your app's callback URL.
Usually it would be something like this::
    
    http://www.myapp.com/odesk_auth/callback/

You will also need to store your pair of oDesk API keys in `settings.py`::
    
    ODESK_PUBLIC_KEY = '(your public key)'
    ODESK_PRIVATE_KEY = '(your private key)'

Most probably you will want to use model-based authentication (the default),
that works with django's built-in `User` model.
To do so, add the `django_odesk.auth.backends.ModelBackend` to your
`AUTHENTICATION_BACKENDS` setting::


    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'django_odesk.auth.backends.ModelBackend',
    )


.. note::

    Please note that `django_odesk.auth` relies on Django sessions mechanism,
    and thus `django.contrib.sessions.middleware.SessionMiddleware` has to be
    enabled

Using authentication
--------------------

To make the user authenticate with oDesk account, point them to the
`django_odesk.auth.views.authenticate` view, like::

    /odesk_auth/authenticate/

That will send the user to odesk.com site for authentication, and log them in
upon redirecting back. 
.. TODO: More on `authenticate` and API token
The user will be asked to log-in at odesk.com, if they are not already, and
to authorize your app, if they use it for the first time.
.. TODO: User model creation 
By default, the new `User` instance will be created for each unknown user. If 
you want to change this, use the `ODESK_CREATE_UNKNOWN_USER` setting::

    ODESK_CREATE_UNKNOWN_USER = False

By default, the `is_staff` and `is_superuser` attributes are both set to False 
for a new user. You can change this (and other aspects of user creation) by 
subclassing the `django_odesk.auth.backends.ModelBackend` and overwriting the
`configure_user` method. However, for a simple cases there is a shortcut: use 
the `ODESK_ADMINS` and `ODESK_SUPERUSERS` lists in `settings.py`::

    ODESK_ADMINS = ('johndoe@odesk.com','janedoe@odesk.com')
    ODESK_SUPERUSERS = ('janedoe@odesk.com',)

Those users will get admin or superuser rights, respectively. These settings 
only have effect on user creation. 

To authenticate the user manualy, use `django.contrib.auth.authenticate()`
with a `token` keyword argument.

Limiting access
---------------

Use the same methods for limiting access, as you would with built-in
`authentication <http://docs.djangoproject.com/en/dev/topics/auth/#limiting-access-to-logged-in-users>`_.

As with Django's built-in authentication, you need to provide a login page
yourself. To make users authenticate with oDesk, you could add line like this
to your `login.html` template::

    Log in with oDesk account <a href="{% url django_odesk.auth.views.authenticate %}?next={{ next }}">here</a>

For simple cases you may just set login page to the 
`django_odesk.auth.views.authenticate`, like this::

    LOGIN_URL = '/odesk_auth/authenticate/'


Authentication without a database
---------------------------------

If for some reason you don't want to use Django's `User` model or the 
database layer at all, you can still use oDesk authentication.
All you need to change is an authentication backend. Use `SimpleBackend`
instead of `ModelBackend`::

    AUTHENTICATION_BACKENDS = (
        'django_odesk.auth.backends.SimpleBackend',
    )

.. note::
    Please note that this type of authentication still relies on 
    `django.contrib.auth.middleware.AuthenticationMiddleware`, although
    it does not require `django.contrib.auth` to be added to the
    `INSTALLED_APPS`

When user authenticates, the `request.user` will be a special object with
an interface similar to that of `django.contrib.auth.models.User`
You may use it much in a way you would use Django's `User` object::

    >>> request.user.username
    'solex@odesk.com'
    >>> request.user.first_name
    'Oleksiy'
    >>> request.user.is_authenticated()
    True

Default values for "security-related" attributes are::

    >>> request.user.is_active
    True
    >>> request.user.is_staff
    False
    >>> request.user.is_superuser
    False

The settings `ODESK_ADMINS` and `ODESK_SUPERUSERS` may be used to change those
values for specified users.
The `ODESK_CREATE_UNKNOWN_USER` setting obviously has no effect.

.. note::
   Please note that, even though you can check for `is_staff` status, you
   cannot use the database-less authentication to access the built-in admin.
   It relies on the database and the built-in `User` model too heavily.




Clients
=======


There are two convenient subclasses of `odesk.Client` which can save you
some typing.

`django_odesk.core.clients.DefaultClient` is already pre-populated with
oDesk API keys from your `settings.py` file. So you can use it like this::
    
    from django_odesk.core.clients import DefaultClient

    client = DefaultClient() #Not authenticated

    # Or

    client = DefaultClient('your_api_token') #Authenticated
    client.team.get_teamrooms()

`django.core.clients.RequestClient` is a subclass of `DefaultClient`, which
takes a `request` parameter. It uses a token from the session and it should be
used in conjunction with `django_odesk.auth`::

    from django_odesk.core.clients import RequestClient

    def my_view(request):
        client = RequestClient(request) #Already authenticated
        client.team.get_teamrooms()
        # ...

If you plan to use odesk API calls extensively in your views, there is 
another shortcut, the `django_odesk.core.middleware.RequestClientMiddleware`.
It populates `request` with `odesk_client` attribute, which is an instance
of `RequestClient`::

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        # ...
        'django_odesk.auth.middleware.AuthenticationMiddleware',
        'django_odesk.core.middleware.RequestClientMiddleware',
    )

Then you may use the client in your views::

    def my_view(request):
        request.odesk_client.team.get_teamrooms()
        # ...

