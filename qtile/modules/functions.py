# Copyright (c) 2024 Technicfan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# _____ _____ ____ _   _ _   _ ___ ____ _____ _    _   _    ____ ____  _____    _  _____ ___ ___  _   _   _
#|_   _| ____/ ___| | | | \ | |_ _/ ___|  ___/ \  | \ | |  / ___|  _ \| ____|  / \|_   _|_ _/ _ \| \ | | | |
#  | | |  _|| |   | |_| |  \| || | |   | |_ / _ \ |  \| | | |   | |_) |  _|   / _ \ | |  | | | | |  \| | | |
#  | | | |__| |___|  _  | |\  || | |___|  _/ ___ \| |\  | | |___|  _ <| |___ / ___ \| |  | | |_| | |\  | |_|
#  |_| |_____\____|_| |_|_| \_|___\____|_|/_/   \_\_| \_|  \____|_| \_\_____/_/   \_\_| |___\___/|_| \_| (_)

import os
import psutil
import subprocess
import alsaaudio
from configparser import ConfigParser
from libqtile.lazy import lazy


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


def get_battery():
    return "bat: " + str(round(psutil.sensors_battery().percent)) + "%"


def get_vram_usage():
    b = int(subprocess.getoutput("nvidia-smi --query-gpu=memory.used \
            --format=csv,noheader,nounits")) * 2**20
    unit = "G"
    match unit:
        case "Mi":
            usage = str(b*2**-20) + "Mi"
        case "Gi":
            usage = str(round(b*2**10, 2)) + "Gi"
        case "M":
            usage = str(round(b*10**-6)) + "M"
        case "G":
            usage = str(round(b*10**-9, 2)) + "G"
    return "vram: " + usage


# window name function
def window_name(name):
    if "- Oracle VM VirtualBox" in name:
        return name.split("[", 1)[0].lower()
    elif name == "web.whatsapp.com":
        return name.split(".")[1]
    else:
        return name.lower()


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
    if way not in "toggle|up|down":
        return
    mixer = alsaaudio.Mixer()
    if way == "toggle":
        mixer.setmute(-(mixer.getmute()[0]-1))
    else:
        step = qtile.widgets_map["volume"].step
        vol = mixer.getvolume()[0]
        diff = vol % step
        if way == "up":
            vol += step - diff
        else:
            if diff != 0:
                vol -= diff
            else:
                vol -= step
        if vol <= 0:
            mixer.setmute(1)
        else:
            mixer.setmute(0)
        mixer.setvolume(vol)
        # volume osd using dunst
        subprocess.run(f"notify-send -a qtile-volume\
            -h string:x-dunst-stack-tag:test -h int:value:{vol}\
                'Volume: {vol}%'", shell=True)
