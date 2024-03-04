import os
import sys
from configparser import ConfigParser
from pathlib import Path
from libqtile.command.client import InteractiveCommandClient

config_file = Path(os.path.expanduser("~/.config/qtile/states/states.ini"))

def check(widget):
    config = ConfigParser()
    config.read(config_file)
    if config["widgetboxes"][widget] == "1":
        return True

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

if not config_file.is_file():

    os.mknod(config_file)

    config = ConfigParser()

    config["widgetboxes"] = {
        "mpris": "0",
        "tray": "0"
    }

    config["screens"] = {
        "screen_state": "1"
    }

    with open(config_file, 'w') as conf:
        config.write(conf)


client = InteractiveCommandClient()

match sys.argv[1]:
    case "mpris":
        match sys.argv[2]:
            case "toggle":
                if not check("tray"):
                    client.widget["mpris"].toggle()          
                if check("mpris"):
                    hidden("mpris")
                else:
                    shown("mpris")
            case "show":
                if not check("tray"):
                    client.widget["mpris"].open()
                shown("mpris")
            case "hide":
                if not check("tray"):
                    client.widget["mpris"].close()
                hidden("mpris")
            case "restore":
                if check("mpris"):
                    client.widget["mpris"].open()
            case "shown":
                shown("mpris")
            case "hidden":
                hidden("mpris")
    case "tray":
        match sys.argv[2]:
            case "toggle":
                if check("mpris"):
                    client.widget["mpris"].toggle()
                client.widget["tray"].toggle()
                if check("tray"):
                    hidden("tray")
                else:
                    shown("tray")
            case "shown":
                shown("tray")
            case "hidden":
                hidden("tray")