
try:
    import settings
except Exception:
    raise Exception("Failed to find a settings.py on your project path. Add settings.py to the root of your project directory")

if not getattr(settings, 'USERNAME', ''):
    raise Exception('No USERNAME specified in settings.py')
if not getattr(settings, 'PROJECTNAME', ''):
    raise Exception('No PROJECTNAME specified in settings.py')

if not hasattr(settings, 'API_KEY') and not hasattr(settings, 'CLIENT_KEY'):
    raise Exception('Not API_KEY or CLIENT_KEY found in settings.py')

if not getattr(settings, 'API_KEY', '') and not getattr(settings, 'CLIENT_KEY', ''):
    raise Exception('No API_KEY or CLIENT_KEY set in settings.py')

import requests
import json

SAVE_URL = 'http://api.botrocket.com/v1/data/save/'

def save(data={}, no_duplicates=False):
    if not data:
        return False
    
    payload = {'client_key': settings.CLIENT_KEY,
        'username': settings.USERNAME,
        'project': settings.PROJECT,
        'collection': 'venues',
        'no_duplicates': no_duplicates,
        'data': json.dumps(data)
    }
    
    resp = requests.post(SAVE_URL, data=payload)
    reply = json.loads(resp.text)
    return reply['status'] == 'OK'
