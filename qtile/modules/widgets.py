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

import getpass
import subprocess

from libqtile import bar, qtile
from libqtile.config import Screen
from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration

from .colors import colors
from .functions import (
    get_battery,
    get_distro,
    get_uptime,
    get_vram_usage,
    toggle_tray,
    volume_up_down,
    window_name,
)


class Clock(widget.Clock):
    def poll(self):
        return super().poll().lower()


class Mpris2(widget.Mpris2):
    def get_track_info(self, metadata) -> str:
        return super().get_track_info(metadata).lower()


def init_widgets():
    widgets_list = [
        widget.GroupBox(
            margin_x=10,
            padding=0,
            borderwidth=0,
            spacing=8,
            active=colors[2],
            block_highlight_text_color=colors[0],
            rounded=False,
            disable_drag=True,
            highlight_method="text",
            urgent_alert_method="line",
            this_current_screen_border=colors[6],
            this_screen_border=colors[9],
            other_current_screen_border=colors[6],
            other_screen_border=colors[9],
            urgent_border=colors[5],
            urgent_text=colors[0],
            hide_unused=True,
            toggle=False,
        ),
        widget.TextBox(text="-", foreground=colors[7], padding=0),
        widget.WindowName(
            foreground=colors[9],
            padding=10,
            max_chars=85,
            width=bar.CALCULATED,
            parse_text=window_name,
            empty_group_string=get_distro("Linux") + " - Qtile".lower(),
        ),
        widget.Prompt(
            foreground=colors[6], cursor_color=colors[0], padding=0, cursorblink=False
        ),
        # Middle of the bar
        widget.Spacer(),
        widget.WidgetBox(
            widgets=[
                widget.modify(
                    Mpris2,
                    padding=7,
                    no_metadata_text="<d-bus> wtf",
                    paused_text="   {track}",
                    format="{xesam:title} - {xesam:artist}",
                    background=colors[0],
                    foreground=colors[8],
                    objname="org.mpris.MediaPlayer2.spotify",
                    width=275,
                    font="VictorMono Nerd Font Bold Italic",
                ),
            ],
            text_closed="",
            text_open="",
            close_button_location="right",
            name="mpris",
            start_opened=True,
        ),
        widget.Spacer(),
        # Middle of the bar
        widget.TextBox(
            padding=2,
            text=subprocess.check_output("printf $(uname -r)", shell=True, text=True),
            # fmt="kernel: {}",
            fmt="  {}",
            foreground=colors[1],
        ),
        widget.CPU(
            padding=12,
            # format="cpu: {load_percent}%",
            format="  {load_percent}%",
            foreground=colors[2],
        ),
        widget.Memory(
            padding=2,
            foreground=colors[5],
            format="{MemUsed: .2f}{mm}",
            measure_mem="G",
            # fmt="ram: {}"
            fmt=" {}",
        ),
        widget.GenPollText(
            padding=12, update_interval=1, func=get_vram_usage, foreground=colors[6]
        ),
        widget.GenPollText(
            padding=2,
            update_interval=30,
            func=get_uptime,
            foreground=colors[7],
            # fmt="up: {}"
            fmt="󰁫 {}",
        ),
        widget.Volume(
            padding=12,
            foreground=colors[8],
            # fmt="vol: {}",
            fmt="  {}",
            step=5,
            mouse_callbacks={
                "Button1": volume_up_down("toggle"),
                "Button4": volume_up_down("up"),
                "Button5": volume_up_down("down"),
            },
        ),
        widget.WidgetBox(
            widgets=[
                widget.modify(
                    Clock,
                    padding=2,
                    foreground=colors[9],
                    format="%a %-d. %B - %-H:%M",
                    mouse_callbacks={"Button1": lazy.spawn("gsimplecal")},
                ),
            ],
            text_closed="",
            text_open="",
            close_button_location="right",
            start_opened=True,
            name="datetime",
        ),
        widget.WidgetBox(
            widgets=[
                widget.Systray(padding=5, icon_theme="Gruvbox-Plus-Dark", icon_size=17)
            ],
            text_closed="",
            text_open="",
            close_button_location="right",
            name="tray",
        ),
        widget.TextBox(
            padding=12,
            foreground=colors[2],
            text=getpass.getuser().lower(),
            mouse_callbacks={
                "Button1": toggle_tray,
                "Button2": lazy.spawn("kitty --name nvim -d GitHub/my-qtile nvim"),
                # "Button3": lazy.spawn(
                #     '.config/qtile/scripts/mouse.sh "Razer Basilisk V3" 0.45'
                # ),
            },
        ),
    ]
    return widgets_list


### SCREEN INITIALISATION ###
def init_screen(screen: int) -> Screen:
    widgets = init_widgets()
    # replace vram widget with battery if nvidia-smi not found
    if subprocess.call("command -v nvidia-smi", shell=True):
        widgets[10].update_interval, widgets[10].func = 30, get_battery

    match screen:
        case 1:
            # replace systray with statusnotifier under wayland
            if qtile.core.name == "wayland":
                widgets[14].widgets[0] = widget.StatusNotifier(
                    padding=7,
                    icon_size=17,
                    icon_theme="Gruvbox-Plus-Dark",
                    highlight_radius=0,
                    show_menu_icons=False,
                    menu_width=250,
                    menu_background=colors[0],
                    highlight_colour=colors[1],
                    menu_foreground=colors[2],
                    menu_foreground_highlighted=colors[0],
                    menu_foreground_disabled=colors[4],
                    separator_colour=colors[4],
                    menu_font="JetBrains Bold",
                )
        case 2:
            # not opening systray when clicking on user on screen2
            widgets[15].mouse_callbacks = {}
            # extend window name on second screen
            widgets[2].max_chars = 125
            # run prompt
            del widgets[3:4]
            # mpris
            del widgets[4:5]
            # systray
            del widgets[12:13]

    return Screen(
        top=bar.Bar(
            widgets=widgets, size=30, background=colors[0], margin=[4, 4, 0, 4]
        ),
        wallpaper=subprocess.getoutput(
            "~/.config/qtile/scripts/dmenu-wallpaper.sh print"
        ),
        wallpaper_mode="fill",
    )


# Some settings that are used on almost every widget
widget_defaults = dict(
    font="VictorMono Nerd Font Bold",
    # font="Sans Bold",
    fontsize=12,
    background=colors[0],
    decorations=[
        RectDecoration(
            line_colour=colors[1], line_width=2, radius=0, filled=False, group=True
        )
    ],
)

### SCREENS ###
screens = [init_screen(i) for i in range(1, 3)]
