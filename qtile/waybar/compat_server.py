import itertools
import subprocess

from flask import Flask
from libqtile.command.base import CommandError, SelectError
from libqtile.command.client import InteractiveCommandClient

client = InteractiveCommandClient()
app = Flask(__name__)


colors = [
    "#282828",
    "#d4be98",
    "#d3869b",
]


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


def get_screen(port):
    screen = 0
    try:
        while True:
            if client.screen[screen].info()["port"] == port:
                break
            else:
                screen += 1
    except SelectError:
        pass
    return screen


@app.route("/groups/<show_all>", methods=["GET"])
def groups(show_all):
    screen = client.group.info()["screen"]
    output = ""
    for group in client.get_groups().values():
        if group["screen"] is not None:
            if group["screen"] == screen:
                output += f"<p>{group['label']}</p>;"
            else:
                output += f"<s>{group['label']}</s>;"
        elif group["label"] != "" and (show_all == "true" or len(group["windows"]) > 0):
            output += f"{group['label']};"
    return output


@app.route("/window/<port>", methods=["GET"])
def window(port):
    try:
        name = client.group[client.get_screens()[get_screen(port)]["group"]].info()[
            "focus"
        ]
        if name is not None:
            return name.lower() + "\n"
        raise CommandError
    except CommandError:
        return get_distro("Linux") + " - Qtile\n".lower()


@app.route("/switch/<label>", methods=["POST"])
def switch(label):
    try:
        for group in client.get_groups().values():
            if group["label"] == label:
                client.group[group["name"]].toscreen(client.screen.info()["index"])
    except CommandError:
        pass
    return ""


@app.route("/cycle/<direction>", methods=["POST"])
def cycle(direction):
    group = client.group.info()
    current = None
    if group is not None:
        current = group["name"]
    i = None
    if direction == "forwards":
        i = itertools.cycle(client.get_groups())
    elif direction == "backwards":
        i = itertools.cycle(reversed(client.get_groups()))
    if i is None:
        return ""
    while next(i) != current:
        pass
    new_group = None
    while (
        new_group is None
        or new_group == "scratchpad"
        or len(client.group[new_group].info()["windows"]) == 0
    ):
        new_group = next(i)
    if len(client.group[new_group].info()["windows"]) > 0:
        client.group[new_group].toscreen(client.screen.info()["index"])
    return ""
