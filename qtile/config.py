import os
import subprocess
from libqtile import hook
from libqtile.config import Screen

from keybindings import mouse, keys
from groups import groups, dgroups_app_rules
from layouts import layouts, floating_layout
from widgets import screens, widget_defaults

### AUTOSTART ###
@hook.subscribe.startup_once
def start_once():
    script = os.path.expanduser("~/.config/qtile/scripts/autostart.sh")
    subprocess.run([script])

### other things ###
dgroups_key_binder = None
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
wl_input_rules = None

# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
