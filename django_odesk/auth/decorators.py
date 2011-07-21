from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group

def group_required(names, login_url=None):
    """
    Checks if the user is a member of a particular group (or at least one
    group from the list)
    """
    if not hasattr(names,'__iter__'):
        names = [names]
    return user_passes_test(lambda u: u.groups.filter(name__in=names),
                            login_url=login_url)
