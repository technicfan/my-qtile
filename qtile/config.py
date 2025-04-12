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

from libqtile import hook
from libqtile.backend.wayland.inputs import InputConfig
from modules.groups import groups  # noqa: F401
from modules.keybindings import keys, mouse  # noqa: F401
from modules.layouts import floating_layout, layouts  # noqa: F401
from modules.widgets import screens, widget_defaults  # noqa: F401


### HOOKS ###
@hook.subscribe.startup_once
def start_once():
    script = os.path.expanduser("~/.config/qtile/scripts/autostart.sh")
    subprocess.run([script])


### OTHER ###
dgroups_key_binder = None
dgroups_app_rules = []  # type: list
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
    "type:mouse": InputConfig(pointer_accel=0),
    "type:keyboard": InputConfig(kb_layout="de"),
}

# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
