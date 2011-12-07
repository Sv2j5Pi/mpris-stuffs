'''mpris_info
code stolen from: https://github.com/duckinator/xchat-mpris/blob/master/xchat-mpris.py
thanks ^_^
'''
import dbus

__credit__ = 'https://github.com/duckinator'

bus = dbus.SessionBus()
bus_name = 'org.mpris.MediaPlayer2.'

def performAction(action, player):
    try:
        remote_object = bus.get_object(bus_name + player, "/Player")
        iface = dbus.Interface(remote_object, "org.freedesktop.MediaPlayer")
        
        fn = getattr(iface, action)
        if fn:
            return fn()
    except dbus.exceptions.DBusException:
        return False

    
# Pass in milliseconds, get (minutes, seconds)
def _parseSongPosition(time):
    return _getMinutesAndSeconds(time / 1000)

# Pass in just seconds, get (minutes, seconds)
def _getMinutesAndSeconds(seconds):
    return (seconds / 60, seconds % 60)

# Pass in both minutes and seconds
def _formatTime(time):
    if time > 0:
        return "%d:%02d" % time
    else:
        return "0:00"

def getSongInfo(player):
    try:
        remote_object = bus.get_object(bus_name + player, "/Player")
        iface = dbus.Interface(remote_object, "org.freedesktop.MediaPlayer")
        
        data = iface.GetMetadata()
        title = data["title"].strip().encode('utf-8')
        album = data["album"].strip().encode('utf-8')
        artist = data["artist"].strip().encode('utf-8')
        pos = _formatTime(_parseSongPosition(iface.PositionGet()))
        length = _formatTime(_getMinutesAndSeconds(data["time"]))
        
        return 'Now playing {} by {} from the album {} [{}/{}]'.format(title, artist, album, pos, length)
    except dbus.exceptions.DBusException:
        return None

def getPlayerVersion(player):
    try:
        remote_object = bus.get_object(bus_name + player, "/")
        iface = dbus.Interface(remote_object, "org.freedesktop.MediaPlayer")
        version = iface.Identity()
      
    except dbus.exceptions.DBusException:
        pass
    return version