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

Finally, you will need  to include the 
`django_odesk.auth.middleware.Authentication` middleware to the list of 
middleware classes::

    
    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        # ...
        'django_odesk.auth.middleware.AuthenticationMiddleware',
    )

.. note::

    Please note that `django_odesk.auth` relies on Django sessions mechanism,
    and thus `django.contrib.sessions.middleware.SessionMiddleware` has to be
    enabled

Using authentication
--------------------

To make the user authenticate with oDesk account, point them to the
`django_odesk.auth.views.authenticate` view::

    /odesk_auth/authenticate/

That will send the user to odesk.com site for authentication, and store
their API authorization token in the session upon redirecting them back.
The user will be asked to log-in at odesk.com, if they are not already, and
to authorize your app, if they use it for the first time.

The `AuthenticationMiddleware` populates the `request` with `odesk_user` 
attribute. It is an instance of `ODeskUser` class with an interface similar
to `django.contrib.auth.models.User`. For non-authenticated user
`request.odesk_user` is an instance of 
`django.contrib.auth.models.AnonymousUser`

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

.. admonition:: Authentication token's life time

    When you obtain an authentication token, you may use it to make API calls
    on behalf of the user.
    Authentication token *never expires* unless explicitly revoked, 
    and it does not depend on user's logged-in status at odesk.com.
    Normally a token is obtained only once and then stored in the session. The 
    user is considered authorized until the session is flushed.
    This may lead to the situation when a user is logged out at odesk.com site,
    but is still logged in as oDesk user at your site. 
    If you need to be sure every time that the user accessing the page is the
    same user that is currently logged in at odesk.com, set
    `settings.ODESK_AUTH_FORCE_RENEWAL` to True. This will initiate a full 
    authentication process for each protected view. Normally that means a
    redirect to odesk.com and back.


Logging out
-----------

Since `django-odesk` uses session to store all auth-related data, using normal
`django.auth.logout()` will revoke oDesk authentication as well.
However, since `dango.auth.logout` doesn't know about the `request.odesk.user`
attribute, it will live until the next request (when it will be set to 
`AnonymousUser` by a middleware).

A proper way to log out an oDesk user is using `django_odesk.auth.logout()` 
function. 
Calling it removes all oDesk auth-related data from the session. It 
*does not* flush the session completely or otherwise affect other 
authentication mechanisms.

.. note::
    Please note that using `django_odesk.auth.logout()` doesn't affect the
    user's logged-in status at odesk.com in any way.


Limiting access
---------------

Limiting access is very similar to that with Django's built-in
authentication.

The raw way::

    from django.http import HttpResponseRedirect

    def my_view(request):
        if not request.odesk_user.is_authenticated():
            return HttpResponseRedirect('/login/?next=%s' % request.path)
        # ...    

Using the decorator::

    from django_odesk.auth.decorators import auth_required

    @auth_required
    def my_view(request):
        # ...    


The `auth_required` decorator works much like Django's `login_required` with 
a few differences:

* It first checks for `settings.ODESK_LOGIN_URL` before the normal 
  `settings.LOGIN_URL`
* Since it is not possible to pass `redirect_to` between requests to 
  odesk.com and back, it stores the last url in the session variable 
  `odesk_redirect_url`, which is then used by a `callback` view


As with Django's built-in authentication, you need to provide a login page
yourself. If you set neither `ODESK_LOGIN_URL` nor `LOGIN_URL`, the 
non-authenticated user will be redirected to the default `/accounts/login/`

You could add the line like this to your `login.html` template::

    Log in with oDesk account <a href="{% url django_odesk.auth.views.authenticate %}">here</a>

If you want to have different pages for normal login and oDesk login,
you may set the `settings.ODESK_LOGIN_URL` variable. This is mostly useful 
for simple applications, when you don't want to display any intermediate page,
but instead send the non-authenticated user directly to the odesk.com for 
authentication. In this case you may write something like this::

    ODESK_LOGIN_URL = '/odesk_auth/authenticate/'


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
used with conjunction with `django_odesk.auth`::

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

