from libqtile.config import Key, KeyChord, Drag, Click
from libqtile.lazy import lazy

from functions import minimize_all
from groups import groups, group_names
from colors import colors, myTerm

mod = "mod4"
myBrowser = "firefox"
myFM = "dolphin"

### KEYBINDINGS ###
keys = [
    # The essentials
    Key([mod], "Return", lazy.spawn(myTerm), desc="Terminal"),
    Key([mod], "b", lazy.spawn(myBrowser), desc="Web browser"),
    Key([mod], "v", lazy.spawn("firefox --private-window"), desc="Web browser private session"),
    Key([mod, "shift"], "Return", lazy.spawn(myFM), desc="File Manager"),
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "h", lazy.hide_show_bar(), desc="Toggle bar"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "l", lazy.spawn("xkill"), desc="Kill GUI apps"),
    Key([mod], "r", lazy.spawncmd(prompt="Run"), desc="Spawn a command using a prompt widget"),
    Key([], "XF86Launch6", lazy.spawn(".config/qtile/scripts/numlock.sh toggle")),
    Key([mod, "shift"], "r", lazy.reload_config(), lazy.spawn(".config/qtile/scripts/widgetboxes.sh mpris restore"), desc="Reload the config"),
    Key([mod, "control"], "r", lazy.restart(), lazy.spawn("sleep 1 && .config/qtile/scripts/widgetboxes.sh mpris restore", shell=True), desc="Restart qtile"),
    Key([mod, "control"], "p", lazy.spawn("kill picom"), lazy.spawn("picom -b --config .config/picom/picom.conf"), desc="Restart picom"),
    Key([mod, "control"], "c", lazy.spawn("clipcatd -r"), desc="Restart clipcat"),

    # dmenu - make sure to apply x,y,z patch and install 'dmenu-extended-git'
    # Dmenu scripts stolen from evil DT
    Key([mod], "o", lazy.spawn(".config/qtile/scripts/dmenu.sh output-switcher"), desc="Change pipewire output"),
    Key([mod], "i", lazy.spawn(".config/qtile/scripts/dmenu.sh kill"), desc="Kill processes"),
    Key([mod], "x", lazy.spawn(".config/qtile/scripts/dmenu.sh logout"), desc="Launch logout script"),
    # own
    Key([mod], "d", lazy.spawn("dmenu_extended_run"), desc="Run launcher"),
    Key([mod], "p", lazy.spawn(".config/qtile/scripts/dmenu.sh monitor"), desc="Monitor configuration"),
    Key([mod], "w", lazy.spawn(".config/qtile/scripts/dmenu.sh ms-windows"), desc="MS Windows (vms/apps)"),
    # cool folder icon color changer
    Key([mod], "minus", lazy.spawn(".config/qtile/scripts/icon-color.sh dmenu"), desc="Change folder colors of gruvbox icon theme"),
    # clipcat
    Key([mod], "c", lazy.spawn("clipcat-menu"), desc="dmenu clipboard manager"),
    # stolen from Luke Smith
    Key([mod], "period", lazy.spawn(".config/qtile/scripts/dmenu.sh unicode"), desc="dmenu emoji picker"),

    # Scratchpads
    Key([mod, "shift"], "o", lazy.group["scratchpad"].dropdown_toggle("mixer"), desc="Toggle sound mixer"),
    Key([mod, "shift"], "t", lazy.group["scratchpad"].dropdown_toggle("term"), desc="Toggle terminal"),
    Key([mod, "shift"], "i", lazy.group["scratchpad"].dropdown_toggle("monitor"), desc="Toggle process monitor"),

    # rgb lighting (key chord SUPER+k followed by "key")
    KeyChord([mod], "k", [
        Key([], "k", lazy.spawn("kill openrgb"),
                     lazy.spawn(".config/qtile/scripts/numlock.sh match && polychromatic-cli -e mouse && polychromatic-cli -e mousepad", shell=True),
                     lazy.spawn("polychromatic-cli -o brightness -p 50"), desc="normal rgb lighting"),
        Key([], "o", lazy.spawn("kill openrgb"), lazy.spawn("polychromatic-cli -o brightness -p 0"), desc="no rgb lighting"),
        Key([], "l", lazy.spawn("polychromatic-cli -o spectrum && openrgb --startminimized", shell=True), desc="rgb lighting as sound visualizer"),
    ]),

    # Screenshot
    Key([], "print", lazy.spawn("flameshot screen"), desc="Screenshot active screen"),
    Key([mod, "shift"], "s", lazy.spawn("flameshot full"), desc="Screenshot all screens"),
    Key([], "XF86Tools", lazy.spawn("flameshot gui"), desc="Snipping tool"),

    # Spotify with three different actions (key chord SUPER+s followed by "key")
    KeyChord([mod], "s", [
        Key([], "s", lazy.spawn("com.spotify.Client && sleep 0.5 && playerctl play-pause", shell=True), lazy.spawn(".config/qtile/scripts/widgetboxes.sh mpris show"), desc="Spotify - auto play"),
        Key([], "q", lazy.spawn("kill spotify"), lazy.spawn(".config/qtile/scripts/widgetboxes.sh mpris hide"), desc="Kill Spotify"),
        Key([], "d", lazy.spawn("com.spotify.Client && .config/qtile/scripts/widgetboxes.sh mpris show", shell=True), desc="Spotify"),
    ]),

    # Media
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause media key"),
    Key([], "XF86AudioPause", lazy.spawn("playerctl play-pause"), desc="Play/Pause media key"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Next media key"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Previous media key"),
    Key([mod], "m", lazy.spawn(".config/qtile/scripts/widgetboxes.sh mpris toggle"), desc="Toggle mpris"), 

    # Volume
    Key([], "XF86AudioRaiseVolume", lazy.widget["volume"].increase_vol(), desc="Raise volume key"),
    Key([], "XF86AudioLowerVolume", lazy.widget["volume"].decrease_vol(), desc="Lower volume key"),
    Key([], "XF86AudioMute", lazy.widget["volume"].mute(), desc="Mute key"),

    # Activate Linux
    KeyChord([mod], "a", [
        Key([], "a", lazy.spawn("activate-linux -x 500 -d -t 'Linux aktivieren' -m 'Wechseln Sie zu den Einstellungen, um Linux zu aktivieren.'"), desc="start activate linux"),
        Key([], "q", lazy.spawn("kill activate-linux"), desc="kill activate linux"),
    ]),
    
    # Switch between windows
    #Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    #Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "right", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "left", lazy.layout.up(), desc="Move focus up"),

    # Move windows between left/right columns or move up/down in current stack.
    #Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    #Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "left", lazy.layout.shuffle_up(), desc="Move window downup"),

    # Window state control
    Key([mod], "t", lazy.window.toggle_floating(), desc="toggle floating"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="toggle fullscreen"),
    Key([mod, "shift"], "m", minimize_all(), desc="Toggle hide/show all windows on current group"),

    # Switch focus of monitors
    Key([mod], "comma", lazy.next_screen(), desc="Move focus to next monitor"),

    # Switch groups
    Key([mod], "Tab", lazy.screen.next_group(), desc="Move to next group"),
    Key([mod], "XF86Launch5", lazy.screen.prev_group(), desc="Move to prev group"),

]

for i in groups:
    if any([i.name in x for x in group_names]):
        keys.extend(
            [
                Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Switch to group {}".format(i.name)),
                Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen(), desc="Move focused window to group {}".format(i.name)),
            ]
        )

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]