#oDesk API keys
ODESK_PUBLIC_KEY = ''
ODESK_PRIVATE_KEY = ''

#Whether a new user should be created if doesn't exist in the DB yet
ODESK_CREATE_UNKNOWN_USER = True

#Setting this to True would prevent the backend from storing the 
#authentication token in the session, so no API calls would be possible.
#Use if all you want is authentication
ODESK_AUTH_ONLY = False

#Define oDesk users who will get staff status when added to the DB
ODESK_ADMINS = ()

#Define oDesk users who will get superuser status when added to the DB
ODESK_SUPERUSERS = ()

#Use to define your own `User` model
ODESK_CUSTOM_USER_MODEL = None

#Whether a new group should be created if doesn't exist in the DB yet
ODESK_CREATE_UNKNOWN_GROUP = True

#Define whether "pseudo-groups" (like company:team:admins) are created
ODESK_CREATE_PSEUDO_GROUPS = False

#Do we want permissions (groups) to be synced with oDesk
#each time user logs in
ODESK_SYNC_PERMISSIONS_ON_LOGIN = False
