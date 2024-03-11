#!/usr/bin/python3

import os
import sys
from configparser import ConfigParser
from pathlib import Path
from libqtile.command.client import InteractiveCommandClient

def init_conf(config_file):
    if not config_file.is_file():
        os.mknod(config_file)
        config = ConfigParser()
        config["widgetboxes"] = {
            "mpris": "0"
        }
        config["screens"] = {
            "screen_state": "1"
        }
        with open(config_file, 'w') as conf:
            config.write(conf)

def main(args):      
    client = InteractiveCommandClient()
    config_file = Path(os.path.expanduser("~/.config/qtile/states/states.ini"))
    init_conf(config_file)
    config = ConfigParser()
    config.read(config_file)
    match args[1]:
        case "restore":
            if config["widgetboxes"]["mpris"] == "1":
                client.widget["mpris"].open()
        case "reset":
            config["widgetboxes"]["mpris"] = "0"
            with open(config_file, 'w') as conf:
                config.write(conf)

main(sys.argv)