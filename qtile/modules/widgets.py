# Copyright (c) 2022 elParaguayo
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
# _____ _____ ____ _   _ _   _ ___ ____ _____ _    _   _    ____ ____  _____    _  _____ ___ ___  _   _   _
#|_   _| ____/ ___| | | | \ | |_ _/ ___|  ___/ \  | \ | |  / ___|  _ \| ____|  / \|_   _|_ _/ _ \| \ | | | |
#  | | |  _|| |   | |_| |  \| || | |   | |_ / _ \ |  \| | | |   | |_) |  _|   / _ \ | |  | | | | |  \| | | |
#  | | | |__| |___|  _  | |\  || | |___|  _/ ___ \| |\  | | |___|  _ <| |___ / ___ \| |  | | |_| | |\  | |_|
#  |_| |_____\____|_| |_|_| \_|___\____|_|/_/   \_\_| \_|  \____|_| \_\_____/_/   \_\_| |___\___/|_| \_| (_)

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

# newest version from git
#make shure to place either a copy of widgetbox.py or a symlink to a copy of it in root config dir
from widgetbox import WidgetBox

from functions import toggle_tray, volume_up_down, window_name, get_uptime
from colors import colors

# Some settings that are used on almost every widget
widget_defaults = dict(
    font="JetBrains Bold",
    fontsize = 12,
)

decoration_group = {
    "decorations": [
        RectDecoration(colour=colors[1], radius=13, filled=True, group=True),
        RectDecoration(colour=colors[0], radius=11, filled=True, group=True, padding=2)
    ]
}

decoration_group2 = {
    "decorations": [
        RectDecoration(colour=colors[1], radius=13, filled=True, group=True),
        RectDecoration(colour=colors[0], radius=11, filled=True, group=True, padding=2),
        RectDecoration(colour=colors[1], radius=13, filled=True, group=True),
    ]
}

def init_widgets_list():
    widgets_list = [
        widget.TextBox(
                 text = "\uf3e2",
                 fontsize = 21,
                 font = "Ubuntu",
                 padding = 7,
                 foreground = colors[0],
                 mouse_callbacks = {"Button1": lazy.spawn("vscodium GitHub/my-qtile")},
                 **decoration_group2
                 ),
        widget.Prompt(
                 foreground = colors[0],
                 cursor_color = colors[0],
                 padding = 3,
                 cursorblink = False,
                 **decoration_group2
        ),
        widget.Spacer(length=2, **decoration_group2),
        widget.CurrentLayoutIcon(
                 foreground = colors[1],
                 padding = 7,
                 scale = 0.7,
                 **decoration_group
                 ),
        widget.Spacer(length=-4, **decoration_group),
        widget.GroupBox(
                 fontsize = 11,
                 margin_x = 4,
                 padding_x = 2,
                 padding_y = 5,
                 borderwidth = 2,
                 active = colors[2],
                 block_highlight_text_color = colors[0],
                 rounded = False,
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
        widget.Spacer(length=-2, **decoration_group),
        widget.WindowName(
                 foreground = colors[2],
                 padding = 10,
                 max_chars = 85,
                 width = bar.CALCULATED,
                 parse_text = window_name,
                 empty_group_string = distro.name() + " - Qtile",
                 **decoration_group 
                 ),

        # Middle of the bar

        widget.Spacer(**decoration_group),
        WidgetBox ( 
             widgets = [
                    widget.Mpris2(
                         padding = 10,
                         no_metadata_text = "D-Bus: wtf",
                         paused_text = "   {track}",
                         format = "{xesam:title} - {xesam:artist}",
                         background = colors[1],
                         foreground = colors[0],
                         objname = "org.mpris.MediaPlayer2.spotify",
                         width = 275,
                         markup = False,
                         **decoration_group2
                    ),
             ],
             text_closed = "",
             text_open = "",
             close_button_location = "right",
             name = "mpris",
             **decoration_group2
        ),
        widget.Spacer(**decoration_group),

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
                 foreground = colors[2],
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
        widget.GenPollText(
                 padding = 10,
                 update_interval = 30,
                 func = get_uptime,
                 foreground = colors[2],
                 fmt = "\uf21e   {}",
                 **decoration_group
                 ),
        widget.Volume(
                 padding = 10,
                 foreground = colors[2],
                 fmt = "🕫  {}",
                 step = 5,
                 mouse_callbacks = {"Button4": volume_up_down("up"), "Button5": volume_up_down("down")},
                 **decoration_group
                 ),
        WidgetBox ( 
             widgets = [
                    widget.Clock(
                             padding = 10,
                             foreground = colors[2],
                             format = "⏱  %a  %d. %B - KW %W - %H:%M",
                             mouse_callbacks = {"Button1": lazy.spawn("galendae")},
                             **decoration_group
                    ),
             ],
             text_closed = "",
             text_open = "",
             close_button_location = "right",
             start_opened = True,
             name = "datetime",
             **decoration_group2
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
                 name = "tray",
                 **decoration_group
        ),
        widget.TextBox(
                 padding = 10,
                 foreground = colors[0],
                 text = getpass.getuser() + "@" + socket.gethostname(),
                 mouse_callbacks = {"Button1": toggle_tray(), "Button3": lazy.spawn('.config/qtile/scripts/mouse.sh "Razer Basilisk V3" 0.45')},
                 **decoration_group2
                 ),
        ]
    return widgets_list

### WIDGET INITIALISATION ###
def init_widgets_colorscheme():
    widgets_colorscheme = init_widgets_list()
    match colors[2]:
        case "#c678dd":
            widgets_colorscheme[3].custom_icon_paths = [".config/qtile/layout-icons/pink"]
        case "#87a757":
            widgets_colorscheme[3].custom_icon_paths = [".config/qtile/layout-icons/green"]
        case "#d3869b":
            widgets_colorscheme[3].custom_icon_paths = [".config/qtile/layout-icons/gruvbox_magenta"]
    return widgets_colorscheme

def init_widgets_screen1():
    widgets_screen1 = init_widgets_colorscheme()
    return widgets_screen1

# Now the python logo, the mpris widget and the systray are removed alongside with some spacers and the user mousecallbacks get removed
def init_widgets_screen2():
    widgets_screen2 = init_widgets_colorscheme()
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
