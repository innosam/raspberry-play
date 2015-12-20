import dbus, keys

class Singleton(object):
    """
    Singleton class by Duncan Booth.
    Multiple object variables refers to the same object.
    http://www.suttoncourtenay.org.uk/duncan/accu/pythonpatterns.html
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

    @classmethod
    def is_initialized(cls):
        print cls._instance
        if cls._instance:
            print "True"
            return True
        print "False"
        return False
          


   
class OmxDbus(Singleton):
    
    def __init__(self):
	self.dbusIfaceKey = None
	self.dbusIfaceProp = None    
        self.initialize_omx_dbus();

    @classmethod
    def is_initialized(cls):
        return super(OmxDbus, cls).is_initialized()
 

    def initialize_omx_dbus(self):
        retry = 0
        try:
            with open('/tmp/omxplayerdbus.root', 'r+') as f:
                omxplayerdbus = f.read().strip()
            bus = dbus.bus.BusConnection(omxplayerdbus)
            object = bus.get_object('org.mpris.MediaPlayer2.omxplayer','/org/mpris/MediaPlayer2', introspect=False)
            self.dbusIfaceProp = dbus.Interface(object,'org.freedesktop.DBus.Properties')
            self.dbusIfaceKey = dbus.Interface(object,'org.mpris.MediaPlayer2.Player')
            done=1
        except:
            retry+=1
            if retry >= 50:
                print "ERROR"
                raise SystemExit
                    
    def send_cmd(self, cmd):
        print self.dbusIfaceProp.PlaybackStatus()
        print self.dbusIfaceProp.Duration()
        print self.dbusIfaceProp.Position()
        print dir(self.dbusIfaceProp)
        if keys.COMMANDS.has_key(cmd):
            self.dbusIfaceKey.Action(dbus.Int32(keys.COMMANDS[cmd]))

    def get_status(self):
        status = ""
        try:
           status = {
           "PlaybackStatus": self.dbusIfaceProp.PlaybackStatus(),
           "Duration" : self.dbusIfaceProp.Duration(),
           "Position" : self.dbusIfaceProp.Position()
	   }
        except:
           pass
        return status