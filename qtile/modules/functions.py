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
"""
from qtile_extras.popup.toolkit import (
    PopupRelativeLayout,
    PopupImage,
    PopupText
)
import calendar
import datetime
"""

# window name function
def window_name(name):
    match name:
        case "- Oracle VM VirtualBox":
            return name.split("[",1)[0]
        case "GLava":
            return ""
        case _:
            return name


# A function for hide/show all the windows in a group
@lazy.function
def minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()


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


"""
# popup calendar
@lazy.function
def show_calendar(qtile):

    day = datetime.datetime.now().day
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    cal = calendar.TextCalendar(calendar.MONDAY).formatmonth(year,month,0,0)

    controls = [
        PopupText(
            text=cal,
            pos_x=0,
            pos_y=0,
            width=1,
            height=1,
        )
    ]

    layout = PopupRelativeLayout(
        qtile,
        width=150,
        height=150,
        controls=controls,
        background="282828",
        initial_focus=None,
    )

    layout.show(x=1575, y=44)
"""