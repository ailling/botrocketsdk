
import settings

BASE_URL = 'http://platform.botrocket.com/api/v1/dev'
METHOD_URL = BASE_URL + '/%s/'

def GetBaseParams(botname=''):
    params = {'username': settings.USERNAME,
              'client_key': settings.CLIENT_KEY,
              'api_key': settings.API_KEY,
              'project': settings.PROJECTNAME}
    
    if botname:
        params['bot'] = botname
    
    return params

def GetURL(method):
    return METHOD_URL % method

