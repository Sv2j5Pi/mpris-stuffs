import dbus

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
def parseSongPosition(time):
    return getMinutesAndSeconds(time / 1000)

# Pass in just seconds, get (minutes, seconds)
def getMinutesAndSeconds(seconds):
    return (seconds / 60, seconds % 60)

# Pass in both minutes and seconds
def formatTime(time):
    if time > 0:
        return "%d:%02d" % time
    else:
        return "0:00"

def getSongInfo(player):
    try:
        remote_object = bus.get_object(bus_name + player, "/Player")
        iface = dbus.Interface(remote_object, "org.freedesktop.MediaPlayer")
        
        #if iface.IsPlaying():
        data = iface.GetMetadata()
        title = data["title"].encode('utf-8')
        album = data["album"].encode('utf-8')
        artist = data["artist"].encode('utf-8')
        pos = formatTime(parseSongPosition(iface.PositionGet()))
        length = formatTime(getMinutesAndSeconds(data["time"]))
        
        return (artist, title, album, pos, length)
        #else:
        #  return 0
    except dbus.exceptions.DBusException:
        return False

def getPlayerVersion(player):
    try:
        remote_object = bus.get_object(bus_name + player, "/")
        iface = dbus.Interface(remote_object, "org.freedesktop.MediaPlayer")
        version = iface.Identity()
      
    except dbus.exceptions.DBusException:
        pass
    return version