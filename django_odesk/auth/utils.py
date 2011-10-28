from django.db import IntegrityError
from django.contrib.auth.models import Group

from django_odesk.core.clients import DefaultClient
from django_odesk.conf import settings

def get_odesk_permissions(auth_token):
    """
    Gets oDesk team roles/permissions for the authenticated user
    """
    client = DefaultClient(auth_token)
    response = client.hr.get_user_role()
    permissions = []
    for record in response['userrole']:
        data = dict(team_id = record['team__id'], role=record['role']) 
        if record['permissions']:
            data['permissions'] = record['permissions']['permission']
        permissions.append(data)
    return permissions



def sync_odesk_permissions(user, auth_token, create_groups=True):
    """
    Syncs oDesk team roles/permissions with Django groups
    """
    permissions = get_odesk_permissions(auth_token)
    user.groups.through.objects.filter(user=user, 
        group__name__contains = '@odesk.com').delete()
    
    def get_or_create_group(name):
        created = False
        group = None
        try:
            group = Group.objects.get(name=name)
        except Group.DoesNotExist:
            if create_groups:
                group = Group(name=name)
                group.save()
        if group:
            user.groups.add(group)
        return group, created 

    for perm in permissions:
        name = '%s@odesk.com' % perm['team_id']
        group, c = get_or_create_group(name=name)
        if settings.ODESK_CREATE_PSEUDO_GROUPS:
            #Adding special groups for admins
            #May later add other pseudo-roles
            if perm['role'] == 'admin':
                name = '%s:%s@odesk.com' % (perm['team_id'], 'admins')
                group, c = get_or_create_group(name=name)
    return True

