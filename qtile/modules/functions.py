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
#  _____ _____ ____ _   _ _   _ ___ ____ _____ _    _   _    ____ ____  _____    _  _____ ___ ___  _   _   _
# |_   _| ____/ ___| | | | \ | |_ _/ ___|  ___/ \  | \ | |  / ___|  _ \| ____|  / \|_   _|_ _/ _ \| \ | | | |
#   | | |  _|| |   | |_| |  \| || | |   | |_ / _ \ |  \| | | |   | |_) |  _|   / _ \ | |  | | | | |  \| | | |
#   | | | |__| |___|  _  | |\  || | |___|  _/ ___ \| |\  | | |___|  _ <| |___ / ___ \| |  | | |_| | |\  | |_|
#   |_| |_____\____|_| |_|_| \_|___\____|_|/_/   \_\_| \_|  \____|_| \_\_____/_/   \_\_| |___\___/|_| \_| (_)

import subprocess

import alsaaudio
import psutil
from libqtile.lazy import lazy


# get distro
def get_distro(default: str):
    try:
        import distro

        return distro.name().lower()
    except ImportError:
        try:
            return subprocess.getoutput(
                "awk -F '=| ' 'NR==1 {print $2}' \
                    <<< \"$((distro || cat /etc/os-release | sed 's/\"//g') 2>/dev/null)\""
            ).lower()
        except Exception:
            return default.lower()


def get_battery():
    return "bat: " + str(round(psutil.sensors_battery().percent)) + "%"


def get_vram_usage(unit="G"):
    b = (
        int(
            subprocess.getoutput(
                "nvidia-smi --query-gpu=memory.used \
            --format=csv,noheader,nounits"
            )
        )
        * 2**20
    )
    match unit:
        case "Mi":
            usage = str(b * 2**-20) + "Mi"
        case "Gi":
            usage = str(round(b * 2**10, 2)) + "Gi"
        case "M":
            usage = str(round(b * 10**-6)) + "M"
        case "G":
            usage = str(round(b * 10**-9, 2)) + "G"
    # return "vram: " + usage
    return "  " + usage


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
            str(seconds % 3600 // 60) + "min ",
        ]
        uptime = ""
        for split in splits:
            if split[0] != "0":
                uptime += split
        return uptime[:-1]


# polychromatic custom effect
def razer_apply_effects(effects: list):
    import polychromatic.procpid as procpid
    from polychromatic.effects import EffectFileManagement

    effectman = EffectFileManagement()

    file_list = effectman.get_item_list()
    for name in effects:
        path = None
        for effect in file_list:
            if effect["name"] == name:
                path = effect["path"]
                break

        if path is not None:
            data = effectman.get_item(path)

            procmgr = procpid.ProcessManager("helper")
            procmgr.start_component(
                ["--run-fx", path, "--device-name", data["map_device"]]
            )


# openrazer dpi
def razer_set_dpi(dpi: int):
    from openrazer.client import DeviceManager

    device_manager = DeviceManager()

    for device in device_manager.devices:
        if device.has("dpi"):
            device.dpi = (dpi, dpi)


# openrazer brightness
def razer_set_brightness(brightness: float):
    from openrazer.client import DeviceManager

    device_manager = DeviceManager()

    for device in device_manager.devices:
        device.brightness = brightness


# set normal on keypress
@lazy.function
def make_lazy(qtile, func, *args):
    func(*args)


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
        mixer.setmute(-(mixer.getmute()[0] - 1))
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
        subprocess.run(
            f"notify-send -a qtile-volume\
            -h string:x-dunst-stack-tag:test -h int:value:{vol}\
                'Volume: {vol}%'",
            shell=True,
        )
