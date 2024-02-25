import os
from libqtile import bar, hook
from libqtile.config import Screen

from keybindings import mouse, keys
from windows_groups import groups, layouts, floating_layout, dgroups_app_rules
from widgets import widgets_screen1, widgets_screen2, widget_defaults

### AUTOSTART ###
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/scripts/autostart.sh"])

### SCREENS ###
screens = [Screen(top=bar.Bar(widgets=widgets_screen1, size=28, margin=4, background="#00000000")),
           Screen(top=bar.Bar(widgets=widgets_screen2, size=28, margin=4, background="#00000000"))]

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
