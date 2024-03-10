# _____ _____ ____ _   _ _   _ ___ ____ _____ _    _   _    ____ ____  _____    _  _____ ___ ___  _   _   _
#|_   _| ____/ ___| | | | \ | |_ _/ ___|  ___/ \  | \ | |  / ___|  _ \| ____|  / \|_   _|_ _/ _ \| \ | | | |
#  | | |  _|| |   | |_| |  \| || | |   | |_ / _ \ |  \| | | |   | |_) |  _|   / _ \ | |  | | | | |  \| | | |
#  | | | |__| |___|  _  | |\  || | |___|  _/ ___ \| |\  | | |___|  _ <| |___ / ___ \| |  | | |_| | |\  | |_|
#  |_| |_____\____|_| |_|_| \_|___\____|_|/_/   \_\_| \_|  \____|_| \_\_____/_/   \_\_| |___\___/|_| \_| (_)

import os
# make shure to install 'python-pyalsaaudio'
import alsaaudio
import subprocess
from configparser import ConfigParser
from libqtile.lazy import lazy

# A function for hide/show all the windows in a group
@lazy.function
def minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()


# stupid widgetboxes script now directly in config (still with file)

def file():
    return os.path.expanduser("~/.config/qtile/states/states.ini")

def shown(widget):
    config = ConfigParser()
    config.read(file())
    config["widgetboxes"][widget] = "1"
    with open(config_file, 'w') as conf:
        config.write(conf)

def hidden(widget):
    config = ConfigParser()
    config.read(file())
    config["widgetboxes"][widget] = "0"
    with open(config_file, 'w') as conf:
        config.write(conf)

def check(widget):
    config = ConfigParser()
    config.read(file())
    if config["widgetboxes"][widget] == "1":
        return True

@lazy.function
def change_mpris(qtile, action):
    match action:
        case "toggle":
            if not qtile.widgets_map["tray"].box_is_open:
                qtile.widgets_map["mpris"].toggle()      

            if qtile.widgets_map["mpris"].box_is_open:
                shown("mpris")
            else:
                hidden("mpris")
        case "open":
            if not qtile.widgets_map["tray"].box_is_open:
                qtile.widgets_map["mpris"].open()
            shown("mpris")
        case "close":
            if not qtile.widgets_map["tray"].box_is_open:
                qtile.widgets_map["mpris"].close()
            hidden("mpris")
        case "restore":
            if check("mpris"):
                qtile.widgets_map["mpris"].open()
        case "reset":
            hidden("mpris")

@lazy.function
def change_tray(qtile, action):
    match action:
        case "toggle":
            if check("mpris"):
                qtile.widgets_map["mpris"].toggle()
            qtile.widgets_map["tray"].toggle()

            if qtile.widgets_map["tray"].box_is_open:
                shown("tray")
            else:
                hidden("tray")
        case "reset":
            hidden("tray")

# volume function
@lazy.function
def volume_up_down(qtile, way):
        m = alsaaudio.Mixer()
        step = qtile.widgets_map["volume"].step
        vol = m.getvolume()[0]
        diff = vol % step
        if way == "up":
            new_vol = vol + step - diff
        if way == "down":
            if diff != 0:
                new_vol = vol - diff
            else:
                new_vol = vol - step
        m.setmute(0)
        m.setvolume(new_vol)
        # volume osd using dunst
        subprocess.call(f"notify-send -a qtile-volume -h string:x-dunst-stack-tag:test -h int:value:{new_vol} 'Volume: {new_vol}%'", shell=True)