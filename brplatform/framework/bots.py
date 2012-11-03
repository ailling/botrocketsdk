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
import helper


class Bot(object):
    "these can be overridden in code, or if not, takes the default specified in the user's account settings"
    
    depends_on = None
    output_to = None
    
    registered_jobs = ['run']
    aggregators = []
    
    def __init__(self, *args, **kwargs):
        self.appname = '%s_%s' % (settings.USERNAME, settings.PROJECTNAME)
        self.botname = self.__class__.__name__
        self.username, self.projectname = self.appname.split('_')
    
    def GetBotName(self):
        return self.botname
    
    def GetAppName(self):
        return self.appname
    
    def GetBotPath(self):
        return ".".join([self.__module__, self.__class__.__name__])
    
    @classmethod
    def register(cls, bot):
        appname = bot.__module__.split('.')[0]
        
        if not hasattr(cls, "_bots"):
            cls._bots = {}
        
        if appname not in cls._bots:
            cls._bots[appname] = set()
        
        cls._bots[appname].add(bot)
        
        print 'bot registered - now have %d' % len(cls._bots[appname])
    
    @classmethod
    def register_standard(cls, bot):
        if not hasattr(cls, "_standardbots"):
            cls._standardbots = set()
        cls._standardbots.add(bot)
        
        print 'bot registered - now have %d' % len(cls._standardbots)
    
    @classmethod
    def GetRegisteredBots(cls, appname):
        if not hasattr(cls, "_bots"):
            cls._bots = {}
        return list(cls._bots.get(appname, set()))
    
    @classmethod
    def GetRegisteredStandardBots(cls):
        if not hasattr(cls, "_standardbots"):
            cls._standardbots = set()
        return list(cls._standardbots)



class ParameterBot(Bot):
    """
    A bot to collect and update parameter lists
    
    BotRocket runs CreateParameters() when the app is initialized (whenever it's pushed to the git repo)
    and UpdateParameters() is pushed into the task queue
    """
    
    def __init__(self, *args, **kwargs):
        super(ParameterBot, self).__init__(*args, **kwargs)
        self.typename = 'ParameterBot'
    
    def StoreParameters(self, botname='', args=[], parameters={}):
        if not args and not parameters:
            return False
        "todo: store parameters in a sandbox environment for the app"
        
        if not botname:
            botname = self.botname
        
        params = helper.GetBaseParams(botname)
        params['args'] = json.dumps(args)
        params['parameters'] = json.dumps(parameters)
        url = helper.GetURL('store-data')
        
        resp = requests.post(url, data=params)
        if resp.text != 'OK':
            raise Exception('Error while saving parameters: %s' % resp.text)
        
        return True


class DataBot(Bot):
    def __init__(self, *args, **kwargs):
        super(DataBot, self).__init__(*args, **kwargs)
        self.typename = 'DataBot'
        self.store = None
    
    
    def QueryData(self, botname=None,
                  time_delta=None, start_timestamp=None, end_timestamp=None,
                  index_delta=None, start_index=None, end_index=None):
        """
        Retrieves data from the sandbox
        """
        if not botname:
            botname = self.botname
        
        params = helper.GetBaseParams(botname)
        extra = {'index_delta': index_delta,
                  'start_index': start_index,
                  'end_index': end_index,
                  
                  'time_delta': time_delta,
                  'start_timestamp': start_timestamp,
                  'end_timestamp': end_timestamp}
        params.update(extra)
        
        url = helper.GetURL('query-data')
        
        resp = requests.get(url, params=params)
        
        data = json.loads(resp.text)
        return data
    
    
    def StoreData(self, data={}):
        """
        Stores data in Bot Rocket's database. Data is not persisted until calling this method
        note in the future the database name should be derived
        from the username
        """
        params = helper.GetBaseParams(self.botname)
        params['data'] = json.dumps(data)
        
        url = helper.GetURL('store-data')
        
        resp = requests.post(url, data=params)
        if resp.text != 'OK':
            raise Exception('Error while storing data: %s' % resp.text)
        
        return data


