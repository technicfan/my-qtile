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
import subprocess
from libqtile import widget, bar
from libqtile.config import Screen
from libqtile.lazy import lazy
from libqtile import qtile
from qtile_extras import widget

from .functions import toggle_tray, volume_up_down, window_name, get_uptime, get_distro, get_vram_usage, toggle_swap
from .colors import colors
from .clock import Clock
from .mpris2widget import Mpris2

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
                 #fontsize = 11,
                 margin_x = 0,
                 padding_x = 0,
                 padding_y = 8,
                 borderwidth = 5,
                 active = colors[2],
                 block_highlight_text_color = colors[0],
                 rounded = False,
                 disable_drag = True,
                 highlight_method = "text",
                 urgent_alert_method = "line",
                 this_current_screen_border = colors[1],
                 this_screen_border = colors[9],
                 other_current_screen_border = colors[1],
                 other_screen_border = colors[9],
                 urgent_border = colors[5],
                 urgent_text = colors[0],
                 hide_unused = True,
                 toggle = False,
                 ),
        widget.WindowName(
                 foreground = colors[9],
                 padding = 3,
                 max_chars = 85,
                 width = bar.CALCULATED,
                 parse_text = window_name,
                 empty_group_string = get_distro("Linux") + " - Qtile".lower(),
                 fmt = "-  {}"
                 ),

        # Middle of the bar

        widget.Spacer(),
        widget.WidgetBox ( 
             widgets = [
                    Mpris2(
                         padding = 7,
                         no_metadata_text = "<d-bus> wtf",
                         paused_text = "   {track}",
                         format = "{xesam:title} - {xesam:artist}",
                         background = colors[0],
                         foreground = colors[8],
                         #objname = "org.mpris.MediaPlayer2.spotifyd",
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
                 padding = 7,
                 text = subprocess.check_output("printf $(uname -r)", shell=True, text=True),
                 #fmt = "\uf17c   {}",
                 fmt = "kernel: {}",
                 foreground = colors[1]
                 ),
        widget.CPU(
                 padding = 7,
                 #format = "\uf2db   {load_percent}%",
                 format = "cpu: {load_percent}%",
                 foreground = colors[2]
                 ),
        widget.Memory(
                 padding = 7,
                 foreground = colors[5],
                 format = "{MemUsed: .2f}{mm}",
                 measure_mem = "G",
                 #fmt = "\uf1c0  {}",
                 fmt = "ram: {}"
                 ),
        widget.WidgetBox(
                 widgets = [
                    widget.Memory(
                    padding = 7,
                    foreground = colors[5],
                    format = "{SwapUsed: .2f}{ms}",
                    measure_swap = "G",
                    #fmt = "\uf1c0  {}"
                    fmt = "swap: {}"
                    ),
                 ],
                 text_closed = "",
                 text_open = "",
                 close_button_location = "right",
                 name = "swap"
        ),
        widget.GenPollText(
                 padding = 7,
                 update_interval = 1,
                 func = get_vram_usage,
                 foreground = colors[6],
                 #fmt = "\uf1c0   {}"
                 fmt = "{}",
                 mouse_callbacks = {"Button1": toggle_swap}
                 ),
        widget.GenPollText(
                 padding = 7,
                 update_interval = 30,
                 func = get_uptime,
                 foreground = colors[7],
                 #fmt = "\uf21e   {}"
                 fmt = "up: {}"
                 ),
        widget.Volume(
                 padding = 7,
                 foreground = colors[8],
                 #fmt = "🕫  {}",
                 fmt = "vol: {}",
                 step = 5,
                 mouse_callbacks = {"Button1": volume_up_down("toggle"),
                                    "Button4": volume_up_down("up"),
                                    "Button5": volume_up_down("down")}
                 ),
        widget.WidgetBox( 
             widgets = [
                    Clock(
                             padding = 7,
                             foreground = colors[9],
                             #format = "⏱  %a  %d. %B - %H:%M",
                             format = "%a  %d. %B - %H:%M",
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
                            padding = 7,
                            icon_theme = "Gruvbox-Plus-Dark",
                            icon_size = 17,
                        ),
                        widget.Spacer(length=3),
                 ],
                 text_closed = "",
                 text_open = "",
                 close_button_location = "right",
                 name = "tray"
        ),
        widget.TextBox(
                 padding = 7,
                 foreground = colors[2],
                 #background = colors[1],
                 #text = (getpass.getuser() + "@" + socket.gethostname()).lower(),
                 text = getpass.getuser().lower(),
                 mouse_callbacks = {"Button1": toggle_tray,
                                    "Button2": lazy.spawn("vscodium GitHub/my-qtile"),
                                    "Button3": lazy.spawn('.config/qtile/scripts/mouse.sh "Razer Basilisk V3" 0.45')
                                   },
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
    # replace systray with statusnotifier under wayland
    if qtile.core.name == "wayland":
        widgets_screen1[14].widgets[0] = widget.StatusNotifier(
            padding = 7, icon_size = 17, icon_theme = "Gruvbox-Plus-Dark",
            highlight_radius = 0, show_menu_icons = False, menu_width = 250,
            menu_background = colors[0], highlight_colour = colors[1],
            menu_foreground = colors[2], menu_foreground_highlighted = colors[0],
            menu_foreground_disabled = colors[4], separator_colour = colors[4],
            menu_font = "JetBrains Bold",
        )
    return widgets_screen1

# Now the python logo, the mpris widget and the systray are removed 
# alongside with some spacers and the user mousecallbacks get removed
def init_widgets_screen2():
    widgets_screen2 = init_widgets_colorscheme()
    # not opening systray when clicking on user on screen2
    widgets_screen2[15].mouse_callbacks = {}
    # extend window name on second screen
    widgets_screen2[2].max_chars = 125
    # run prompt
    del widgets_screen2[0:1]
    # mpris
    del widgets_screen2[3:4]
    # systray
    del widgets_screen2[12:13]
    return widgets_screen2


### SCREENS ###
screens = [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=28, background=colors[0]),
                  wallpaper=subprocess.getoutput("~/.config/qtile/scripts/dmenu-wallpaper.sh print"),
                  wallpaper_mode='fill'),
           Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=28, background=colors[0]), 
                  wallpaper=subprocess.getoutput("~/.config/qtile/scripts/dmenu-wallpaper.sh print"),
                  wallpaper_mode='fill')]
