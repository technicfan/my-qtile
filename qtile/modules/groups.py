# ____  _____ ____ _____ ____   _____   __   ____    _    ____ ___ _____  _    _     ___ ____  __  __   _
#|  _ \| ____/ ___|_   _|  _ \ / _ \ \ / /  / ___|  / \  |  _ \_ _|_   _|/ \  | |   |_ _/ ___||  \/  | | |
#| | | |  _| \___ \ | | | |_) | | | \ V /  | |     / _ \ | |_) | |  | | / _ \ | |    | |\___ \| |\/| | | |
#| |_| | |___ ___) || | |  _ <| |_| || |   | |___ / ___ \|  __/| |  | |/ ___ \| |___ | | ___) | |  | | |_|
#|____/|_____|____/ |_| |_| \_\\___/ |_|    \____/_/   \_\_|  |___| |_/_/   \_\_____|___|____/|_|  |_| (_)

import re
from libqtile.config import Group, Match, ScratchPad, DropDown, Rule

from colors import colors, myTerm

### GROUPS ###
groups = []

group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

group_layouts = ["spiral", "spiral", "spiral", "spiral", "spiral", "spiral", "spiral", "spiral", "max", "spiral"]

#group_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]
#group_labels = ["Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "Ⅷ", "Ⅸ",]
group_labels = ["Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "DEV", "CHAT", "VM", "MUS",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i],
            label=group_labels[i],
        ))

### SCRATCHPADS ###
groups.append(
    ScratchPad("scratchpad", [ DropDown("mixer", "pavucontrol", width=0.5, height=0.5, x=0.25, y=0.1, opacity=1, on_focus_lost_hide=False),
                               DropDown("term", myTerm, width=0.5, height=0.5, x=0.25, y=0.1, opacity=1, on_focus_lost_hide=False),
                               DropDown("proc-monitor", "gnome-system-monitor", width=0.55, height=0.6, x=0.225, y=0.1, opacity=1, on_focus_lost_hide=False),
                               DropDown("bluetooth", "blueman-manager", width=0.5, height=0.5, x=0.225, y=0.1, opacity=1, on_focus_lost_hide=False),
                             ]),
)

### WINDOW RULES ###
dgroups_app_rules = [
    Rule(Match(wm_class=re.compile(r"^(spotify)$")), group="0"),
    Rule(Match(wm_class=re.compile(r"^(VirtualBox\ Machine|spicy|virt\-manager)$")), group="9"),
    Rule(Match(title=re.compile(r"^(VirtualBoxVM)$")), group="9"),
    Rule(Match(wm_class=re.compile(r"^(discord)$")), group="8"),
    Rule(Match(wm_class=re.compile(r"^(vscodium|delphi32.exe)$")), group="7"),
]