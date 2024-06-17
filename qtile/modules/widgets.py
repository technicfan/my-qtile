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
from qtile_extras import widget

from functions import toggle_tray, volume_up_down, window_name, get_uptime
from colors import colors

# Some settings that are used on almost every widget
widget_defaults = dict(
    font="JetBrains Bold",
    fontsize = 12,
    background = colors[0]
)

def init_widgets_list():
    widgets_list = [
        widget.Prompt(
                 foreground = colors[0],
                 background = colors[1],
                 cursor_color = colors[0],
                 padding = 5,
                 cursorblink = False
        ),
        widget.GroupBox(
                 fontsize = 11,
                 margin_x = 0,
                 padding_x = 2,
                 padding_y = 8,
                 borderwidth = 4,
                 active = colors[2],
                 block_highlight_text_color = colors[0],
                 rounded = False,
                 disable_drag = True,
                 highlight_method = "block",
                 urgent_alert_method = "line",
                 this_current_screen_border = colors[1],
                 this_screen_border = colors [2],
                 other_current_screen_border = colors[1],
                 other_screen_border = colors[2],
                 hide_unused = True,
                 toggle = False
                 ),
        widget.Spacer(length=8),
        widget.CurrentLayoutIcon(
                 padding = 0,
                 scale = 0.7
                 ),
        widget.WindowName(
                 foreground = colors[2],
                 padding = 10,
                 max_chars = 85,
                 width = bar.CALCULATED,
                 parse_text = window_name,
                 empty_group_string = distro.name() + " - Qtile"
                 ),

        # Middle of the bar

        widget.Spacer(),
        widget.WidgetBox ( 
             widgets = [
                    widget.Mpris2(
                         padding = 10,
                         no_metadata_text = "<d-bus> wtf",
                         paused_text = "   {track}",
                         format = "{xesam:title} - {xesam:artist}",
                         background = colors[1],
                         foreground = colors[0],
                         objname = "org.mpris.MediaPlayer2.spotify",
                         width = 275,
                         #mouse_callbacks = {"Button4": None, "Button5": None}
                    ),
             ],
             text_closed = "",
             text_open = "",
             close_button_location = "right",
             name = "mpris"
        ),
        widget.Spacer(),

        # Middle of the bar

        widget.TextBox(
                 padding = 10,
                 text = subprocess.check_output("printf $(uname -r)", shell=True, text=True),
                 fmt = "\uf17c   {}",
                 foreground = colors[2]
                 ),
        widget.CPU(
                 padding = 10,
                 format = "\uf2db   {load_percent}%",
                 foreground = colors[2]
                 ),
        widget.Memory(
                 padding = 10,
                 foreground = colors[2],
                 format = "{MemUsed: .2f}{mm}",
                 measure_mem = "G",
                 fmt = "\uf1c0  {}"
                 ),
        widget.GenPollText(
                 padding = 10,
                 update_interval = 30,
                 func = get_uptime,
                 foreground = colors[2],
                 fmt = "\uf21e   {}"
                 ),
        widget.Volume(
                 padding = 10,
                 foreground = colors[2],
                 fmt = "🕫  {}",
                 step = 5,
                 mouse_callbacks = {"Button1": volume_up_down("toggle"), "Button4": volume_up_down("up"), "Button5": volume_up_down("down")}
                 ),
        widget.WidgetBox ( 
             widgets = [
                    widget.Clock(
                             padding = 10,
                             foreground = colors[2],
                             format = "⏱  %a  %d. %B - %H:%M",
                             mouse_callbacks = {"Button1": lazy.spawn("galendae")}
                    ),
             ],
             text_closed = "",
             text_open = "",
             close_button_location = "right",
             start_opened = True,
             name = "datetime"
        ),
        widget.WidgetBox( 
                 widgets = [
                        widget.Systray(
                            padding = 10,
                            icon_theme = "Gruvbox Plus Dark"
                        ),
                        widget.Spacer(length=6),
                 ],
                 text_closed = "",
                 text_open = "",
                 close_button_location = "right",
                 name = "tray"
        ),
        widget.TextBox(
                 padding = 10,
                 foreground = colors[0],
                 background = colors[1],
                 text = getpass.getuser() + "@" + socket.gethostname(),
                 mouse_callbacks = {"Button1": toggle_tray,
                                    "Button2": lazy.spawn("vscodium GitHub/my-qtile"),
                                    "Button3": lazy.spawn('.config/qtile/scripts/mouse.sh "Razer Basilisk V3" 0.45')
                                   }
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
    widgets_screen2[15].mouse_callbacks = {}
    # extend window name on second screen
    widgets_screen2[4].max_chars = 125
    # run prompt
    del widgets_screen2[0:1]
    # mpris
    del widgets_screen2[5:6]
    # systray
    del widgets_screen2[12:13]
    return widgets_screen2


### SCREENS ###
screens = [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=28, background="#282828")),
           Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=28, background="#282828"))]
