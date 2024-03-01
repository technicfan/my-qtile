# ____  _____ ____ _____ ____   _____   __   ____    _    ____ ___ _____  _    _     ___ ____  __  __   _
#|  _ \| ____/ ___|_   _|  _ \ / _ \ \ / /  / ___|  / \  |  _ \_ _|_   _|/ \  | |   |_ _/ ___||  \/  | | |
#| | | |  _| \___ \ | | | |_) | | | \ V /  | |     / _ \ | |_) | |  | | / _ \ | |    | |\___ \| |\/| | | |
#| |_| | |___ ___) || | |  _ <| |_| || |   | |___ / ___ \|  __/| |  | |/ ___ \| |___ | | ___) | |  | | |_|
#|____/|_____|____/ |_| |_| \_\\___/ |_|    \____/_/   \_\_|  |___| |_/_/   \_\_____|___|____/|_|  |_| (_)

import getpass
import socket
# make sure 'python-distro' is installed
import distro
import subprocess
from libqtile import widget, bar
from libqtile.config import Screen
from libqtile.lazy import lazy
# Make sure 'qtile-extras' is installed or this config will not work.
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration

# newest version of it
#make shure to place either a copy of widgetbox.py or a symlink to a copy of it in root config dir
from widgetbox import WidgetBox

from functions import ReplaceWindowName
from colors import colors

# Some settings that are used on almost every widget
widget_defaults = dict(
    font="JetBrains Bold",
    fontsize = 12,
)

decoration_group = {
    "decorations": [
        RectDecoration(colour=colors[1], radius=10, filled=True, group=True),
        RectDecoration(colour=colors[0], radius=8, filled=True, group=True, padding=2)
    ]
}

def init_widgets_list():
    widgets_list = [
        widget.TextBox(
                 text = "\uf3e2",
                 fontsize = 21,
                 font = "Ubuntu",
                 padding = 7,
                 foreground = colors[2],
                 mouse_callbacks = {"Button1": lazy.spawn("vscodium GitHub/my-qtile-and-picom-config")},
                 **decoration_group
                 ),
        widget.Prompt(
                 foreground = colors[1],
                 cursor_color = "#87a757",
                 padding = 3,
                 cursorblink = False,
                 **decoration_group
        ),
        widget.Spacer(length=-2, **decoration_group),
        widget.CurrentLayoutIcon(
                 foreground = colors[1],
                 padding = 7,
                 scale = 0.7,
                 custom_icon_paths = [".config/qtile/layout-icons/green"],
                 decorations = [
                         RectDecoration(colour=colors[1], radius=10, filled=True, group=True),
                         RectDecoration(colour=colors[0], radius=8, filled=True, group=True, padding=2),
                 ]
                 ),
        widget.Spacer(length=-2, **decoration_group),
        widget.GroupBox(
                 fontsize = 11,
                 margin_x = 4,
                 padding_y = 2,
                 padding_x = 2,
                 borderwidth = 2,
                 active = colors[1],
                 inactive = colors[2],
                 block_highlight_text_color = colors[0],
                 rounded = True,
                 disable_drag = True,
                 highlight_method = "block",
                 this_current_screen_border = colors[1],
                 this_screen_border = colors [2],
                 other_current_screen_border = colors[1],
                 other_screen_border = colors[2],
                 hide_unused = True,
                 toggle = False,
                 **decoration_group
                 ),
        widget.Spacer(length=-4, **decoration_group),
        widget.WindowName(
                 foreground = colors[2],
                 padding = 10,
                 max_chars = 85,
                 width = bar.CALCULATED,
                 parse_text = ReplaceWindowName,
                 empty_group_string = distro.name() + " - Qtile",
                 **decoration_group 
                 ),

        # Middle of the bar

        widget.Spacer(
            #**decoration_group
        ),
        WidgetBox ( 
             widgets = [
                    widget.Mpris2(
                         padding = 10,
                         no_metadata_text = "D-Bus: wtf",
                         paused_text = "   {track}",
                         format = "{xesam:title} - {xesam:artist}",
                         foreground = colors[0],
                         #foreground = colors[1],
                         objname = "org.mpris.MediaPlayer2.spotify",
                         width = 250,
                         markup = False,
                         mouse_callbacks = {"Button3": lazy.spawn(".config/qtile/scripts/widgetboxes.sh mpris shown")},
                         #**decoration_group
                         decorations = [
                              RectDecoration(colour=colors[1], radius=10, filled=True, group=True)
                         ]
                    ),
             ],
             text_closed = "",
             text_open = "",
             close_button_location = "right",
             name = "mpris",
             start_opened = False,
             #**decoration_group
        ),
        widget.Spacer(
            #**decoration_group
        ),

        # Middle of the bar

        widget.TextBox(
                 padding = 10,
                 text = subprocess.check_output("printf $(uname -r)", shell=True, text=True),
                 fmt = "\uf17c   {}",
                 foreground = colors[2],
                 **decoration_group
                 ),
        widget.CPU(
                 padding = 10,
                 format = "\uf2db   {load_percent}%",
                 foreground = colors[1],
                 **decoration_group
                 ),
        widget.Memory(
                 padding = 10,
                 foreground = colors[2],
                 format = "{MemUsed: .2f}{mm}",
                 measure_mem = "G",
                 fmt = "\uf1c0  {}",
                 **decoration_group
                 ),
        widget.GenPollCommand(
                 padding = 10,
                 update_interval = 30,
                 cmd = ".config/qtile/scripts/uptime.sh",
                 foreground = colors[1],
                 fmt = "\uf21e   {}",
                 **decoration_group
                 ),
        widget.Volume(
                 padding = 10,
                 foreground = colors[2],
                 fmt = "🕫  {}",
                 step = 5,
                 volume_up_command = ".config/qtile/scripts/volume.sh up 5",
                 volume_down_command = ".config/qtile/scripts/volume.sh down 5",
                 get_volume_command = ".config/qtile/scripts/volume.sh get 5",
                 **decoration_group
                 ),
        widget.Clock(
                 padding = 10,
                 foreground = colors[1],
                 format = "⏱  %a  %d. %B - KW %W - %H:%M",
                 mouse_callbacks = {"Button1": lazy.spawn(".config/qtile/scripts/galendae.sh")},
                 **decoration_group
                 ),
        WidgetBox( 
                 widgets = [
                        widget.Systray(
                                 padding = 5,
                                 **decoration_group
                        ),
                        widget.Spacer(length=6, **decoration_group),
                 ],
                 text_closed = "",
                 text_open = "",
                 close_button_location = "right",
                 **decoration_group
        ),
        widget.TextBox(
                 padding = 10,
                 foreground = colors[2],
                 text = getpass.getuser() + "@" + socket.gethostname(),
                 mouse_callbacks = {"Button1": lazy.spawn(".config/qtile/scripts/widgetboxes.sh systray toggle"), "Button3": lazy.spawn('.config/qtile/scripts/mouse.sh "Razer Basilisk V3" 0.45')},
                 **decoration_group
                 ),
        ]
    return widgets_list

### WIDGET INITIALISATION ###
# Monitor 1 will display ALL widgets in widgets_list. It is important that this
# is the only monitor that displays all widgets because the systray widget will
# crash if you try to run multiple instances of it.
def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    # color for layout icon
    if colors[1] == "#dfbf8e":
        widgets_screen1[3].custom_icon_paths = [".config/qtile/layout-icons/gruvbox"]
    if colors[1] == "#87a757":
        widgets_screen1[3].custom_icon_paths = [".config/qtile/layout-icons/green"]
    return widgets_screen1

# Now the python logo, the mpris widget and the systray are removed alongside with some spacers and the user mousecallbacks get removed
def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    # color for layout icon
    if colors[1] == "#dfbf8e":
        widgets_screen2[3].custom_icon_paths = [".config/qtile/layout-icons/gruvbox"]
    if colors[1] == "#87a757":
        widgets_screen2[3].custom_icon_paths = [".config/qtile/layout-icons/green"]
    # not opening systray when clicking on user on screen2
    widgets_screen2[18].mouse_callbacks = {}
    # python logo
    del widgets_screen2[0:3]
    # mpris
    del widgets_screen2[7:8]
    # systray
    del widgets_screen2[13:14]
    return widgets_screen2


### SCREENS ###
screens = [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=28, margin=[8, 8, 4, 8], background="#00000000")),
           Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=28, margin=[8, 8, 4, 8], background="#00000000"))]