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


# window name function
def window_name(name):
    if "- Oracle VM VirtualBox" in name:
        return name.split("[",1)[0]
    elif name == "web.whatsapp.com":
        return "WhatsApp"
    else:
        return name


# A function for hide/show all the windows in a group
@lazy.function
def minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()


# get uptime
def get_uptime():
    with open("/proc/uptime", "r") as f:
        seconds = int(f.readline().split(".")[0])
    if seconds < 60:
        return "under 1min"
    else:
        splits = [
            str(seconds // 86400) + "d ",
            str(seconds % 86400 // 3600) + "h ",
            str(seconds % 3600 // 60) + "min "
        ]
        uptime = ""
        for split in splits:
            if split[0] != "0":
                uptime += split
        return uptime[:-1]


# widgetboxes functions
@lazy.function
def change_mpris(qtile, action):
    config = ConfigParser()
    config_file = os.path.expanduser("~/.config/qtile/states/states.ini")
    config.read(config_file)
    match action:
        case "toggle":
            qtile.widgets_map["mpris"].toggle()
            if qtile.widgets_map["mpris"].box_is_open:
                config["widgetboxes"]["mpris"] = "1"
            else:
                config["widgetboxes"]["mpris"] = "0"
        case "open":
            qtile.widgets_map["mpris"].open()
            config["widgetboxes"]["mpris"] = "1"
        case "close":
            qtile.widgets_map["mpris"].close()
            config["widgetboxes"]["mpris"] = "0"
    with open(config_file, 'w') as conf:
         config.write(conf)

@lazy.function
def toggle_tray(qtile):
    qtile.widgets_map["tray"].toggle()
    qtile.widgets_map["datetime"].toggle()


# volume function
@lazy.function
def volume_up_down(qtile, way):
        mixer = alsaaudio.Mixer()
        if way == "toggle":
            if mixer.getmute()[0] == 1:
                mixer.setmute(0)
            else:
                mixer.setmute(1)
        else:
            step = qtile.widgets_map["volume"].step
            vol = mixer.getvolume()[0]
            mod = vol % step
            if way == "up":
                new_vol = vol + step - mod
            if way == "down":
                if mod != 0:
                    new_vol = vol - mod
                else:
                    new_vol = vol - step
            if new_vol <= 0:
                mixer.setmute(1)
            else:
                mixer.setmute(0)
            mixer.setvolume(new_vol)
            # volume osd using dunst
            subprocess.call(f"notify-send -a qtile-volume\
                -h string:x-dunst-stack-tag:test -h int:value:{new_vol}\
                    'Volume: {new_vol}%'", shell=True)