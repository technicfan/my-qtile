# Copyright (c) 2024 Technicfan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
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

from libqtile.config import Click, Drag, Key, KeyChord
from libqtile.lazy import lazy

from .functions import (
    make_lazy,
    razer_apply_effects,
    razer_set_brightness,
    volume_up_down,
)
from .groups import group_names

mod = "mod4"
myBrowser = "librewolf"
myFM = "dolphin"
myTerm = "kitty"

### KEYBINDINGS ###
keys = [
    # The essentials
    Key([mod], "Return", lazy.spawn(myTerm), desc="Terminal"),
    Key([mod], "b", lazy.spawn(myBrowser), desc="Web browser"),
    Key(
        [mod],
        "v",
        lazy.spawn("librewolf --private-window"),
        desc="Web browser private session",
    ),
    Key([mod, "shift"], "Return", lazy.spawn(myFM), desc="File Manager"),
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "h", lazy.hide_show_bar(), desc="Toggle bar"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "l", lazy.spawn("xkill"), desc="Kill GUI apps"),
    Key(
        [mod],
        "r",
        lazy.spawncmd(prompt=" Run".lower()),
        desc="Spawn a command using a prompt widget",
    ),
    Key(
        [mod, "shift"],
        "r",
        lazy.reload_config(),
        desc="Reload the config",
    ),
    Key(
        [mod, "control"],
        "r",
        lazy.restart(),
        desc="Restart qtile",
    ),
    Key([mod, "control"], "c", lazy.spawn("clipcatd -r"), desc="Restart clipcat"),
    # dmenu - make sure to apply x,y,z + height + border patch
    Key(
        [mod],
        "o",
        lazy.spawn(".config/qtile/scripts/dmenu.sh output-switcher"),
        desc="Change pipewire output",
    ),
    Key(
        [mod],
        "i",
        lazy.spawn(".config/qtile/scripts/dmenu.sh kill"),
        desc="Kill processes",
    ),
    Key(
        [mod],
        "x",
        lazy.spawn(".config/qtile/scripts/dmenu.sh logout"),
        desc="Launch logout script",
    ),
    # own
    Key([mod], "d", lazy.spawn("l7-dmenu-desktop"), desc="Run launcher"),
    Key(
        [mod],
        "p",
        lazy.spawn(".config/qtile/scripts/dmenu.sh screens"),
        desc="Monitor configuration",
    ),
    Key(
        [mod],
        "w",
        lazy.spawn(".config/qtile/scripts/dmenu.sh vms"),
        desc="Dirty solution for aliases",
    ),
    Key(
        [mod],
        "n",
        lazy.spawn(".config/qtile/scripts/dmenu.sh wallpaper"),
        desc="Change wallpaper",
    ),
    Key(
        [mod],
        "g",
        lazy.spawn(".config/qtile/scripts/dmenu.sh git-repos"),
        desc="Open repo with vscodium",
    ),
    # cool folder icon color changer
    Key(
        [mod],
        "minus",
        lazy.spawn(".config/qtile/scripts/dmenu.sh icon-color"),
        desc="Change folder colors of gruvbox icon theme",
    ),
    # clipcat
    Key([mod], "c", lazy.spawn("clipcat-menu"), desc="dmenu clipboard manager"),
    Key(
        [mod],
        "numbersign",
        lazy.spawn("clipcat-menu --config .config/clipcat/clipcat-menu-rm.toml remove"),
        desc="remove items from clipboard history",
    ),
    Key(
        [mod],
        "adiaeresis",
        lazy.spawn(".config/qtile/scripts/dmenu.sh clear-clipcat"),
        desc="remove all items from clipboard history",
    ),
    # stolen from Luke Smith
    Key(
        [mod],
        "period",
        lazy.spawn(".config/qtile/scripts/dmenu.sh unicode"),
        desc="dmenu emoji picker",
    ),
    # menu-qalc
    Key(
        [mod],
        "plus",
        lazy.spawn(".config/qtile/scripts/menu-qalc.sh"),
        desc="dmenu calculator",
    ),
    # Scratchpads
    Key(
        [mod, "shift"],
        "o",
        lazy.group["scratchpad"].dropdown_toggle("mixer"),
        desc="Toggle sound mixer",
    ),
    Key(
        [mod, "shift"],
        "t",
        lazy.group["scratchpad"].dropdown_toggle("term"),
        desc="Toggle terminal",
    ),
    Key(
        [mod, "shift"],
        "i",
        lazy.group["scratchpad"].dropdown_toggle("proc-monitor"),
        desc="Toggle process monitor",
    ),
    Key(
        [mod, "shift"],
        "p",
        lazy.group["scratchpad"].dropdown_toggle("bluetooth"),
        desc="Toggle bluetooth manager",
    ),
    Key(
        [mod],
        "m",
        lazy.group["scratchpad"].dropdown_toggle("spotify"),
        desc="Toggle Spotify",
    ),
    # rgb lighting (key chord SUPER+k followed by "key")
    KeyChord(
        [mod],
        "k",
        [
            Key(
                [],
                "k",
                make_lazy(razer_apply_effects, ["mouse", "keyboard"]),
                make_lazy(razer_set_brightness, 50),
                desc="normal rgb lighting",
            ),
            Key(
                [],
                "o",
                lazy.spawn("kill openrgb"),
                make_lazy(razer_set_brightness, 0),
                desc="no rgb lighting",
            ),
        ],
    ),
    # Screenshot
    Key([], "print", lazy.spawn("flameshot screen"), desc="Screenshot active screen"),
    Key(
        [mod, "shift"], "s", lazy.spawn("flameshot full"), desc="Screenshot all screens"
    ),
    Key([], "XF86Tools", lazy.spawn("flameshot gui"), desc="Snipping tool"),
    # Spotify (key chord SUPER+s followed by "key")
    KeyChord(
        [mod],
        "s",
        [
            Key(
                [],
                "s",
                lazy.group["scratchpad"].dropdown_toggle("spotify"),
                lazy.spawn("sleep 0.5 && playerctl play-pause", shell=True),
                desc="Spotify - auto play",
            ),
            Key([], "q", lazy.spawn("kill spotify"), desc="Kill Spotify"),
        ],
    ),
    Key(
        [mod],
        "u",
        lazy.spawn(".config/qtile/scripts/ollama.sh"),
        desc="unload all ollama models",
    ),
    Key(
        [mod, "control"],
        "v",
        lazy.spawn(".config/qtile/scripts/unirich.py"),
        desc="cool",
    ),
    # Media
    Key(
        [],
        "XF86AudioPlay",
        lazy.spawn("playerctl play-pause"),
        desc="Play/Pause media key",
    ),
    Key(
        [],
        "XF86AudioPause",
        lazy.spawn("playerctl play-pause"),
        desc="Play/Pause media key",
    ),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Next media key"),
    Key(
        [], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Previous media key"
    ),
    Key([mod, "shift"], "m", lazy.widget["mpris"].toggle(), desc="Toggle mpris"),
    # Volume
    Key([], "XF86AudioRaiseVolume", volume_up_down("up"), desc="Increase volume key"),
    Key([], "XF86AudioLowerVolume", volume_up_down("down"), desc="Decrease volume key"),
    Key([], "XF86AudioMute", volume_up_down("toggle"), desc="Mute key"),
    # Activate Linux
    KeyChord(
        [mod],
        "a",
        [
            Key(
                [],
                "a",
                lazy.spawn(
                    "activate-linux -x 500 -d -t 'Linux aktivieren' -m 'Wechseln Sie zu den Einstellungen, um Linux zu aktivieren.'"
                ),
                desc="start activate linux",
            ),
            Key([], "q", lazy.spawn("kill activate-linux"), desc="kill activate linux"),
        ],
    ),
    # Switch between windows
    # Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    # Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "left", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "right", lazy.layout.up(), desc="Move focus up"),
    # Move windows between left/right columns or move up/down in current stack.
    # Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    # Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "left", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_up(), desc="Move window up"),
    # Window size control
    Key([mod, "control"], "right", lazy.layout.grow(), desc="Grow window"),
    Key([mod, "control"], "left", lazy.layout.shrink(), desc="Shrink window"),
    Key([mod, "control"], "n", lazy.layout.reset(), desc="Shrink window"),
    # Window state control
    Key([mod], "t", lazy.window.toggle_floating(), desc="toggle floating"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="toggle fullscreen"),
    # Switch focus of monitors
    Key([mod], "comma", lazy.next_screen(), desc="Move focus to next monitor"),
    # Switch groups
    Key([mod], "Tab", lazy.screen.next_group(), desc="Move to next group"),
    Key([mod], "XF86Launch5", lazy.screen.prev_group(), desc="Move to prev group"),
]

for group in group_names:
    keys.extend(
        [
            Key(
                [mod],
                group,
                lazy.group[group].toscreen(),
                desc="Switch to group {}".format(group),
            ),
            Key(
                [mod, "shift"],
                group,
                lazy.window.togroup(group),
                lazy.group[group].toscreen(),
                desc="Move focused window to group {}".format(group),
            ),
        ]
    )

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Drag(
        [mod, "shift"],
        "Button1",
        lazy.window.set_position(),
        start=lazy.window.get_position(),
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]
