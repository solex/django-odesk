#oDesk API keys
ODESK_PUBLIC_KEY = ''
ODESK_PRIVATE_KEY = ''

#Whether a new user should be created if doesn't exist in the DB yet
ODESK_CREATE_UNKNOWN_USER = True

#Define oDesk users who will get staff status when added to the DB
ODESK_ADMINS = ()

#Define oDesk users who will get superuser status when added to the DB
ODESK_SUPERUSERS = ()

#Use to define your own `User` model
ODESK_CUSTOM_USER_MODEL = None

#Whether a new group should be created if doesn't exist in the DB yet
ODESK_CREATE_UNKNOWN_GROUP = True

#Do we want permissions (groups) to be synced with oDesk
#each time user logs in
ODESK_SYNC_PERMISSIONS_ON_LOGIN = False
