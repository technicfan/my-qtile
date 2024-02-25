import re
from libqtile import layout
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
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

### SCRATCHPADS ###
groups.append(
    ScratchPad("scratchpad", [ DropDown("mixer", "pavucontrol", width=0.5, height=0.5, x=0.25, y=0.1, opacity=1, on_focus_lost_hide=False),
                               DropDown("term", myTerm, width=0.5, height=0.5, x=0.25, y=0.1, opacity=1, on_focus_lost_hide=False),
                               DropDown("monitor", "gnome-system-monitor", width=0.55, height=0.6, x=0.225, y=0.1, opacity=1, on_focus_lost_hide=False),
                             ]),
)

### LAYOUTS ###
layouts = [
    layout.Spiral(
        main_pane = "left",
        clockwise = True,
        new_client_position = "after_current",
        ratio = 0.5,
        ratio_increment = 0,
        border_width = 2,
        margin = [4, 8, 8, 8],
        border_focus = colors[1],
        border_normal = colors[3]
    ),
    layout.Max(),
]

floating_layout = layout.Floating(
    border_focus=colors[1],
    border_normal=colors[3],
    border_width=2,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),   # gitk
        Match(wm_class="dialog"),         # dialog boxes
        Match(wm_class="download"),       # downloads
        Match(wm_class="error"),          # error msgs
        Match(wm_class="file_progress"),  # file progress boxes
        Match(wm_class="kdenlive"),       # kdenlive
        Match(wm_class="makebranch"),     # gitk
        Match(wm_class="maketag"),        # gitk
        Match(wm_class="notification"),   # notifications
        Match(wm_class="pinentry-gtk-2"), # GPG key password entry
        Match(wm_class="ssh-askpass"),    # ssh-askpass
        Match(wm_class="toolbar"),        # toolbars
        Match(wm_class="Yad"),            # yad boxes
        Match(title="branchdialog"),      # gitk
        Match(title="Confirmation"),      # tastyworks exit box
        Match(title="Qalculate!"),        # qalculate-gtk
        Match(title="pinentry"),          # GPG key password entry
        Match(title="tastycharts"),       # tastytrade pop-out charts
        Match(title="tastytrade"),        # tastytrade pop-out side gutter
        Match(title="tastytrade - Portfolio Report"), # tastytrade pop-out allocation
        Match(wm_class="tasty.javafx.launcher.LauncherFxApp"), # tastytrade settings
        Match(wm_class="delphi32.exe"), # Delphi 7 IDE
        Match(wm_class="quickgui"), # quickemu gui vm manger
    ]
)

### WINDOW RULES ###
dgroups_app_rules = [
    Rule(Match(title=re.compile(r"^(Spotify)$")), group="0"),
    Rule(Match(wm_class=re.compile(r"^(VirtualBox\ Machine|spicy|virt\-manager)$")), group="9"),
    Rule(Match(title=re.compile(r"^(VirtualBoxVM)$")), group="9"),
    Rule(Match(wm_class=re.compile(r"^(discord)$")), group="8"),
    Rule(Match(wm_class=re.compile(r"^(vscodium|delphi32.exe)$")), group="7"),
]