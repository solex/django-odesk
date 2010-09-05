from django.contrib.auth.models import AnonymousUser

def logout(request):
    if 'odesk_api_token' in request.session:
        del request.session['odesk_api_token']
        del request.session['odesk_auth_user_data']
    if 'odesk_api_token_renew' in request.session:
        del request.session['odesk_api_token_renew']
    if hasattr(request, 'odesk_user'):
        request.odesk_user = AnonymousUser()
