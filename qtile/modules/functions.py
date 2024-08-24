# _____ _____ ____ _   _ _   _ ___ ____ _____ _    _   _    ____ ____  _____    _  _____ ___ ___  _   _   _
#|_   _| ____/ ___| | | | \ | |_ _/ ___|  ___/ \  | \ | |  / ___|  _ \| ____|  / \|_   _|_ _/ _ \| \ | | | |
#  | | |  _|| |   | |_| |  \| || | |   | |_ / _ \ |  \| | | |   | |_) |  _|   / _ \ | |  | | | | |  \| | | |
#  | | | |__| |___|  _  | |\  || | |___|  _/ ___ \| |\  | | |___|  _ <| |___ / ___ \| |  | | |_| | |\  | |_|
#  |_| |_____\____|_| |_|_| \_|___\____|_|/_/   \_\_| \_|  \____|_| \_\_____/_/   \_\_| |___\___/|_| \_| (_)

import os
import subprocess
from configparser import ConfigParser
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# guess terminal
def get_term(default: str):
    term = guess_terminal()
    if term == None:
        term = default
    return term

# get distro
def get_distro(default: str):
    try:
        import distro
        return distro.name().lower()
    except:
        try:
            return subprocess.getoutput("awk -F '=| ' 'NR==1 {print $2}' \
                    <<< \"$((distro || cat /etc/os-release | sed 's/\"//g') 2>/dev/null)\"").lower()
        except:
            return default.lower()

def get_vram_usage():
    try:
        import psutil
        return "bat: " + str(round(psutil.sensors_battery().percent)) + "%"
    except:
        b = int(subprocess.getoutput("nvidia-smi --query-gpu=memory.used \
                --format=csv,noheader,nounits")) * 2**20
        unit = "G"
        match unit:
            case "Mi":
                usage = str(b*2**-20) + "Mi"
            case "Gi":
                usage = str(round(b*2**10,2)) + "Gi"
            case "M":
                usage = str(round(b*10**-6)) + "M"
            case "G":
                usage = str(round(b*10**-9,2)) + "G"
        return "vram: " + usage

# window name function
def window_name(name):
    if "- Oracle VM VirtualBox" in name:
        return name.split("[",1)[0].lower()
    elif name == "web.whatsapp.com":
        return name.split(".")[1]
    else:
        return name.lower()


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

@lazy.function
def toggle_swap(qtile):
    config = ConfigParser()
    config_file = os.path.expanduser("~/.config/qtile/states/states.ini")
    config.read(config_file)
    if qtile.widgets_map["mpris"].box_is_open and \
        config["widgetboxes"]["mpris"] == "1" and \
         not qtile.widgets_map["swap"].box_is_open:
        qtile.widgets_map["mpris"].close()
    elif config["widgetboxes"]["mpris"] == "1" and \
          not qtile.widgets_map["mpris"].box_is_open and \
           qtile.widgets_map["swap"].box_is_open:
        qtile.widgets_map["mpris"].open()
    qtile.widgets_map["swap"].toggle()


# volume function
@lazy.function
def volume_up_down(qtile, way):
        if way not in "toggle|up|down":
            return
        try:
            import alsaaudio
        except:
            subprocess.call("notify-send -a qtile\
                'Install pyalsaaudio to control the volume'", shell=True)
            return
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

myTerm = get_term("alacritty")