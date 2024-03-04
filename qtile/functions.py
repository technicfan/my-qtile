# ____  _____ ____ _____ ____   _____   __   ____    _    ____ ___ _____  _    _     ___ ____  __  __   _
#|  _ \| ____/ ___|_   _|  _ \ / _ \ \ / /  / ___|  / \  |  _ \_ _|_   _|/ \  | |   |_ _/ ___||  \/  | | |
#| | | |  _| \___ \ | | | |_) | | | \ V /  | |     / _ \ | |_) | |  | | / _ \ | |    | |\___ \| |\/| | | |
#| |_| | |___ ___) || | |  _ <| |_| || |   | |___ / ___ \|  __/| |  | |/ ___ \| |___ | | ___) | |  | | |_|
#|____/|_____|____/ |_| |_| \_\\___/ |_|    \____/_/   \_\_|  |___| |_/_/   \_\_____|___|____/|_|  |_| (_)

import os
from configparser import ConfigParser
from libqtile.lazy import lazy

# A function for hide/show all the windows in a group
@lazy.function
def minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()


# stupid widgetboxes script now directly in config(still with file)

config_file = os.path.expanduser("~/.config/qtile/states/states.ini")

def shown(widget):
    config = ConfigParser()
    config.read(config_file)
    config["widgetboxes"][widget] = "1"
    with open(config_file, 'w') as conf:
        config.write(conf)

def hidden(widget):
    config = ConfigParser()
    config.read(config_file)
    config["widgetboxes"][widget] = "0"
    with open(config_file, 'w') as conf:
        config.write(conf)

def check(widget):
    config = ConfigParser()
    config.read(config_file)
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