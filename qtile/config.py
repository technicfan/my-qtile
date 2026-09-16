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

import os
import subprocess

from libqtile import hook, qtile
from libqtile.backend.base.window import Window
from libqtile.backend.wayland.inputs import InputConfig
from libqtile.group import _Group
from libqtile.scratchpad import ScratchPad
from modules.functions import (
    myMusicPlayer,
    razer_apply_effects,
    razer_set_brightness,
    razer_set_dpi,
)
from modules.groups import groups  # noqa: F401
from modules.keybindings import keys, mouse  # noqa: F401
from modules.layouts import floating_layout, layouts  # noqa: F401
from modules.widgets import screens, widget_defaults  # noqa: F401


### HOOKS ###
@hook.subscribe.startup_once
def start_once():
    subprocess.run(
        [os.path.expanduser("~/.config/qtile/scripts/autostart.sh")], check=False
    )
    try:
        razer_apply_effects(["mouse", "keyboard"])
        razer_set_brightness(50)
        razer_set_dpi(2300)
    except ImportError:
        pass


@hook.subscribe.shutdown
def shutdown():
    subprocess.run(["kill", "-9", "uwsgi"], check=False)


@hook.subscribe.client_new
def new_client(client: Window):
    classes = client.get_wm_class()
    if classes is not None:
        match classes[0]:
            case myMusicPlayer.wm_class:
                scratchpad: ScratchPad = qtile.groups_map["scratchpad"]
                scratchpad._spawn(scratchpad._dropdownconfig["music"])
            case "flameshot":
                if qtile.core.name == "wayland":
                    client.static()
                    client.enable_floating()
                    client.set_position_floating(0, 0)
                    client.enable_fullscreen()


@hook.subscribe.setgroup
@hook.subscribe.screen_change
@hook.subscribe.client_managed
def group_change(event=None):
    open(os.path.expanduser("~/.config/qtile/waybar/group-change"), "r").close()


@hook.subscribe.focus_change
@hook.subscribe.client_name_updated
def window_change(client=None):
    open(os.path.expanduser("~/.config/qtile/waybar/window-change"), "r").close()


@hook.subscribe.client_managed
def client_managed(client: Window):
    if qtile.core.name == "wayland" and isinstance(client, Window):
        if qtile.current_window is not None and client.group != qtile.current_group:
            qtile.current_window.focus(cursor_warp)
        if client.is_transient_for() is not None:
            client.center()
            client.bring_to_front()
        elif client.group is not None and client.group.name == "6":
            client.float_x = 0
            client.float_y = 0
            client.enable_fullscreen()
        elif client.name == "gsimplecal":
            client.set_position_floating(1726, 25)


@hook.subscribe.float_change
def float_change():
    if qtile.core.name == "wayland":
        gaming_group: _Group = qtile.groups_map["6"]
        gaming_group.unminimize_all()
        # if qtile.current_group.name != "6":
        #     for window in gaming_group.windows:
        #         if (
        #             window.float_x == 0
        #             and window.float_y == 0
        #             and not window.fullscreen
        #         ):
        #             window.enable_fullscreen()
        #         if window.float_x is None and window.float_y is None:
        #             window.float_x = 0
        #             window.float_y = 0


@hook.subscribe.client_name_updated
def name_updated(client: Window):
    classes = client.get_wm_class()
    if classes is not None:
        match classes[0]:
            case "librewolf":
                if (
                    qtile.core.name == "wayland"
                    and "Bitwarden" in client.name
                    and "Erweiterung" in client.name
                ):
                    client.enable_floating()
                    if not hasattr(client, "_bw_positioned"):
                        client.center()
                        client._bw_positioned = True


### OTHER ###
dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = "floating_only"
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = False

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = {
    "type:pointer": InputConfig(accel_profile="flat", pointer_accel=0),
    "type:touchpad": InputConfig(tap=True),
    "type:keyboard": InputConfig(kb_layout="de", kb_variant="nodeadkeys"),
}

idle_timers = [
    # IdleTimer(
    #     10,
    #     action=lambda: qtile.core.hide_cursor(),
    #     resume=lambda: qtile.core.unhide_cursor(),
    # ),
]

# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
