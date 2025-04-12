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

import re

from libqtile.config import DropDown, Group, Match, ScratchPad

# temporary solution
myTerm = "kitty"

### GROUPS ###
groups = []

group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

group_layouts = [
    "spiral",
    "spiral",
    "spiral",
    "spiral",
    "spiral",
    "spiral",
    "spiral",
    "spiral",
    "spiral",
    "max",
]

group_matches = [
    [Match(wm_class=re.compile(r"^(firefox|firefox-esr|LibreWolf)$"))],
    [],
    [],
    [],
    [Match(wm_class=re.compile(r"^joplin$"))],
    [Match(wm_class=re.compile(r"^Minecraft\* .*$"))],
    [
        Match(
            wm_class=re.compile(
                r"^(no-risk-client|prismlauncher|lunarclient|minecraft-launcher|Minecraft Linux Launcher UI)$"
            )
        )
    ],
    [Match(wm_class=re.compile(r"^(vscodium|delphi32.exe|nvim)$"))],
    [
        Match(
            wm_class=re.compile(
                r"^(discord|signal|WebApp-WhatsApp5304|WebApp-ChatGPT6070|GPT4All|lm studio|fluffychat|element|WebApp-Cinny7844|WebApp-OllamaWebUI0953)$"
            ),
            title="Alpaca",
        )
    ],
    [
        Match(wm_class=re.compile(r"^(VirtualBox\ Machine|virt\-manager|vmware)$")),
        Match(title=re.compile(r"^(VirtualBoxVM)$")),
    ],
]

# group_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
# group_labels = ["Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "Ⅷ", "Ⅸ", "X"]
# group_labels = ["Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "DEV", "CHAT", "VM", "MUS"]
# group_labels = ["Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "DEV", "CHAT", "VM"]
group_labels = ["WEB", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "DEV", "CHAT", "VM"]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i],
            label=group_labels[i].lower(),
            matches=group_matches[i],
        )
    )

### SCRATCHPADS ###
groups.append(
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "mixer",
                "pavucontrol",
                width=0.5,
                height=0.5,
                x=0.25,
                y=0.1,
                opacity=1,
                on_focus_lost_hide=False,
            ),
            DropDown(
                "term",
                myTerm,
                width=0.5,
                height=0.5,
                x=0.25,
                y=0.1,
                opacity=1,
                on_focus_lost_hide=False,
            ),
            DropDown(
                "proc-monitor",
                "gnome-system-monitor",
                width=0.55,
                height=0.6,
                x=0.225,
                y=0.1,
                opacity=1,
                on_focus_lost_hide=False,
            ),
            DropDown(
                "bluetooth",
                "blueman-manager",
                width=0.5,
                height=0.5,
                x=0.225,
                y=0.1,
                opacity=1,
                on_focus_lost_hide=False,
            ),
            DropDown(
                "spotify",
                "com.spotify.Client",
                match=Match(wm_class="spotify"),
                width=0.9,
                height=0.85,
                x=0.05,
                y=0.05,
                opacity=1,
                on_focus_lost_hide=True,
            ),
        ],
    ),
)
