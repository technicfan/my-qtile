# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
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

import os
import getpass
import socket
# make sure 'python-distro' is installed
import distro
import subprocess
from libqtile import bar, extension, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
# Make sure 'qtile-extras' is installed or this config will not work.
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration, RectDecoration
from qtile_extras.popup.templates.mpris2 import COMPACT_LAYOUT, DEFAULT_LAYOUT
import colors

mod = "mod4"              # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"      # My terminal of choice
myBrowser = "firefox"     # My browser of choice
myFM = "dolphin"          # My filemanager of choice

# A function for hide/show all the windows in a group
@lazy.function
def minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()
            
@lazy.function
def maximize_by_switching_layout(qtile):
    current_layout_name = qtile.current_group.layout.name
    if current_layout_name == "monadtall":
        qtile.current_group.layout = "max"
    elif current_layout_name == "max":
        qtile.current_group.layout = "monadtall"

# Dmenu theme
dmenu_theme = {
    "background": "#133912",
    "foreground": "#87a757",
    "selected_background": "#87a757",
    "selected_foreground": "#133912",
    "dmenu_font": "JetBrains:Bold:pixelsize=14",
    "dmenu_ignorecase": True,
    "dmenu_lines": "20",
}

# A list of available commands that can be bound to keys can be found
# at https://docs.qtile.org/en/latest/manual/config/lazy.html
keys = [
    # The essentials
    Key([mod], "Return", lazy.spawn(myTerm), desc="Terminal"),
    Key([mod], "b", lazy.spawn(myBrowser), desc="Web browser"),
    Key([mod], "c", lazy.spawn("firefox --private-window"), desc="Private web browser"),
    Key([mod, "shift"], "Return", lazy.spawn(myFM), desc="File Manager"),
    Key(["control"], "escape", lazy.spawn("ksysguard"), desc="Process explorer"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "r", lazy.spawncmd(prompt="run"), desc="Spawn a command using a prompt widget"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),

    # dmenu
    Key([mod], "x", lazy.spawn("dm-logout"), desc="Launch logout script"),
    Key([mod], "d", lazy.run_extension(extension.DmenuRun(
        dmenu_command = "dmenu_run -z 473",
        dmenu_prompt = "Run:",
        **dmenu_theme,
    )), desc="Run launcher"),
    Key([mod], "w", lazy.run_extension(extension.CommandSet(
        dmenu_command = "dmenu -z 473",
        dmenu_prompt = "Extra Apps:",
        commands = {
            "Delphi 7": "wine .wine/drive_c/Program\ Files\ \(x86\)/Borland/Delphi7/Bin/delphi32.exe",
            "Discord": "com.discordapp.Discord",
            "Tor Browser": "torbrowser-launcher",
            "ATT": "archlinux-tweak-tool",
            "Writer": "libreoffice --writer",
            "Impress": "libreoffice --impress",
            "Calc": "libreoffice --calc",
            "BiBox": "chromium --app=https://bibox2.westermann.de/shelf",
            "Minecraft Bedrock Launcher": "/home/technicfan/Applications/Minecraft_Bedrock_Launcher-x86_64-v0.11.4.721_6a112963f5b0815232f9127d54eef130.AppImage",
            "GPT4All": "/mnt/Games/gpt4all/bin/chat",
            "Stable Diffusion WebUI": "alacritty -e /home/technicfan/stable-diffusion-webui/webui.sh",
            "Sunshine": "sunshine",
        },
        **dmenu_theme,
    )), desc="Run launcher with extra apps"),
    Key([mod], "p", lazy.run_extension(extension.CommandSet(
        dmenu_command = "dmenu -p 'Monitors:' -z 473",
        commands = {
            "Monitor 1": ".config/qtile/scripts/one-screen.sh",
            "Both Monitors": ".config/qtile/scripts/two-screens.sh",
            "Mirror": "xrandr --output DP-4 --auto --output HDMI-0 --auto --same-as DP-4",
            "Off": "xrandr --output HDMI-0 --off --output DP-4 --off",
        },
        **dmenu_theme,
    )), desc="Monitor configuration"),

    # Lock
    Key([mod], "l", lazy.spawn("i3lock-fancy-dualmonitor"), desc="Lock screen"),

    # Keyboard
    KeyChord([mod], "k", [
        Key([], "k", lazy.spawn("kill openrgb"), lazy.spawn("polychromatic-cli -o spectrum"), lazy.spawn("polychromatic-cli -o brightness -p 50"), desc="normal rgb lighting"),
        Key([], "o", lazy.spawn("kill openrgb"), lazy.spawn("polychromatic-cli -o brightness -p 0"), desc="no rgb lighting"),
        Key([], "l", lazy.spawn("openrgb --startminimized"), desc="rgb lighting as sound visualizer"),
    ]),

    # Github
    Key([mod], "g", lazy.spawn("github-desktop"), desc="GitHub desktop"),

    # Screenshot
    Key([], "print", lazy.spawn("flameshot screen"), desc="Screenshot active screen"),
    Key([], "scroll_lock", lazy.spawn("flameshot full"), desc="Screenshot all screens"),
    Key([mod, "shift"], "s", lazy.spawn("flameshot gui"), desc="Snipping tool"),

    # Spotify
    KeyChord([mod], "s", [
        Key([], "s", lazy.spawn("com.spotify.Client && sleep 0.5 && playerctl play-pause", shell=True), desc="Spotify - auto play"),
        Key([], "q", lazy.spawn("kill spotify"), desc="Kill Spotify"),
        Key([], "d", lazy.spawn("com.spotify.Client"), desc="Spotify"),
    ]),

    #Media
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause media key"),
    Key([], "XF86AudioPause", lazy.spawn("playerctl play-pause"), desc="Play/Pause media key"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Next media key"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Previous media key"),
    Key([mod], "m", lazy.widget["widgetbox"].toggle(), desc="Toggle mpris"), 

    #Volume
    Key([], "XF86AudioRaiseVolume", lazy.widget["volume"].increase_vol(), desc="Raise volume key"),
    Key([], "XF86AudioLowerVolume", lazy.widget["volume"].decrease_vol(), desc="Lower volume key"),
    Key([], "XF86AudioMute", lazy.widget["volume"].mute(), desc="Mute key"),

    # Activate Linux
    KeyChord([mod], "a", [
        Key([], "a", lazy.spawn("activate-linux -x 500 -d -t 'Linux aktivieren' -m 'Wechseln Sie zu den Einstellungen, um Linux zu aktivieren.'"), desc="start activate linux"),
        Key([], "q", lazy.spawn("kill activate-linux"), desc="kill activate linux"),
    ]),
    
    # Switch between windows
    Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window downup"),

    # window state control
    Key([mod], "t", lazy.window.toggle_floating(), desc="toggle floating"),
    Key([mod], "f", maximize_by_switching_layout(), lazy.window.toggle_fullscreen(), desc="toggle fullscreen"),
    Key([mod, "shift"], "m", minimize_all(), desc="Toggle hide/show all windows on current group"),

    # Switch focus of monitors
    Key([mod], "period", lazy.next_screen(), desc="Move focus to next monitor"),
    Key([mod], "comma", lazy.prev_screen(), desc="Move focus to prev monitor"),
    
    # Dmenu scripts launched using the key chord SUPER+o followed by "key"
    KeyChord([mod], "o", [
        Key([], "h", lazy.spawn("dm-hub"), desc="List all dmscripts"),
        Key([], "c", lazy.spawn("dm-confedit"), desc="Choose a config file to edit"),
        Key([], "k", lazy.spawn("dm-kill"), desc="Kill processes"),
        Key([], "p", lazy.spawn("dm-pipewire-out-switcher"), desc="Change pipewire output")
    ]),

]
groups = []
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

#group_labels = ["DEV", "WWW", "SYS", "DOC", "VBOX", "CHAT", "MUS", "VID", "GFX",]
#group_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]
#group_labels = ["", "", "", "", "", "", "", "", "",]
#group_labels = ["Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "Ⅷ", "Ⅸ",]
#group_labels = ["Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "</>", " ", " ", " ",]
group_labels = ["Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "DEV", "GIT", "WIN", "MUS",]


group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall"]


for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))
 
for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
        ]
    )


# Window rules
@hook.subscribe.client_new
def client_new(client):
    if client.name == "Spotify":
        client.togroup("0"),
    if client.name == "Default - Wine desktop":
        client.togroup("9"),
    if client.name == "GitHub Desktop":
        client.togroup("8"),
    if client.name == "VSCodium":
        client.togroup("7"),

### COLORSCHEME ###
# Colors are defined in a separate 'colors.py' file.

colors = colors.Technicfan

### LAYOUTS ###
# Some settings that I use on almost every layout, which saves us
# from having to type these out for each individual layout.
layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": colors[1],
                "border_normal": colors[3]
                }

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(
         border_width = 0,
         margin = 4,
         ),
]

# Some settings that I use on almost every widget, which saves us
# from having to type these out for each individual widget.
widget_defaults = dict(
    font="JetBrains Bold",
    fontsize = 12,
    #background=colors[0]
)

decoration_group = {
    "decorations": [
        RectDecoration(colour=colors[1], radius=10, filled=True, group=True),
        RectDecoration(colour=colors[0], radius=8, filled=True, group=True, padding=2)
    ]
}

groupboxes = {
    "fontsize": 11,
    "margin_x": 4,
    "padding_y": 2,
    "padding_x": 2,
    "borderwidth": 2,
    "active": colors[2],
    "inactive": colors[1],
    "block_highlight_text_color": colors[0],
    "rounded": True,
    "disable_drag": True,
    "highlight_method": "block",
    "this_current_screen_border": colors[1],
    "this_screen_border": colors [2],
    "other_current_screen_border": colors[1],
    "other_screen_border": colors[2],
    "use_mouse_wheel": False,
}

widgetbox_systray = widget.WidgetBox( 
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
                    )

widgetbox_mpris = widget.WidgetBox ( 
                     widgets = [
                             widget.Mpris2(
                                 padding = 10,
                                 no_metadata_text = "Keine Metadaten",
                                 paused_text = "Pausiert: {track}",
                                 format = "{xesam:title} - {xesam:artist}",
                                 foreground = colors[1],
                                 width = 250,
                                 decorations = [
                                     RectDecoration(colour=colors[2], radius=10, filled=True, group=True),
                                     RectDecoration(colour=colors[0], radius=8, filled=True, group=True, padding=2)
                                 ]
                             ),
                     ],
                     text_closed = "",
                     text_open = "",
                     close_button_location = "right"
                  )

extension_defaults = widget_defaults.copy()


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
                 **decoration_group
        ),
        widget.Spacer(length=-2, **decoration_group),
        widget.GroupBox(
                 visible_groups = ["1", "2", "3", "4", "5", "6"],
                 **groupboxes,
                 **decoration_group
                 ),
        widget.Spacer(length=-4, **decoration_group),
        widget.GroupBox(
                 visible_groups = ["7", "8", "9", "0"],
                 hide_unused = True,
                 **groupboxes,
                 **decoration_group
                 ),
        widget.Spacer(length=-2, **decoration_group),
        widget.WindowName(
                 foreground = colors[2],
                 padding = 10,
                 max_chars = 70,
                 width = bar.CALCULATED,
                 empty_group_string = distro.name() + " - Qtile",
                 **decoration_group 
                 ),
        widget.Spacer(),

        # Middle of the bar

        widgetbox_mpris,

        # Middle of the bar

        widget.Spacer(),
        widget.TextBox(
                 padding = 10,
                 text = "\uf17c   " + subprocess.check_output("printf $(uname -r)", shell=True, text=True),
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
                 format = "{MemUsed: .0f}{mm}",
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
                 **decoration_group
                 ),
        widget.Clock(
                 padding = 10,
                 foreground = colors[1],
                 format = "⏱  %d.%m.%Y - %H:%M",
                 **decoration_group
                 ),
        widgetbox_systray,
        widget.TextBox(
                 padding = 10,
                 foreground = colors[2],
                 text = getpass.getuser() + "@" + socket.gethostname(),
                 mouse_callbacks = {"Button1": widgetbox_systray.toggle, "Button3": lazy.spawn(".config/qtile/scripts/mouse.sh")},
                 **decoration_group
                 ),
        ]
    return widgets_list

# Monitor 1 will display ALL widgets in widgets_list. It is important that this
# is the only monitor that displays all widgets because the systray widget will
# crash if you try to run multiple instances of it.
def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

# Now the python logo, the mpris widget and the systray are removed alongside with some spacers and the user mousecallbacks get removed
def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    # not opening systray when clicking on user on screen2
    widgets_screen2[18].mouse_callbacks = {}
    # python logo
    del widgets_screen2[0:3]
    # mpris
    del widgets_screen2[7:8]
    # systray
    del widgets_screen2[13:14]
    return widgets_screen2

# For adding transparency to your bar, add (background="#00000000") to the "Screen" line(s)
# For ex: Screen(top=bar.Bar(widgets=init_widgets_screen2(), background="#00000000", size=24)),
def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=28, margin=[4, 4, 0, 4], background="#00000000")),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=28, margin=[4, 4, 0, 4], background="#00000000"))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_focus=colors[1],
    border_width=2,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),   # gitk
        Match(wm_class="dialog"),         # dialog boxes
        Match(wm_class="download"),       # downloads
        Match(wm_class="error"),          # error msgs
        Match(wm_class="file_progress"),  # file progress boxes
        Match(wm_class="kdenlive"),       # kdenlive
        Match(wm_class="makebranch"),     # gitk
        Match(wm_class="maketag"),        # gitk
        Match(wm_class="notification"),   # notifications
        Match(wm_class="pinentry-gtk-2"), # GPG key password entry
        Match(wm_class="ssh-askpass"),    # ssh-askpass
        Match(wm_class="toolbar"),        # toolbars
        Match(wm_class="Yad"),            # yad boxes
        Match(title="branchdialog"),      # gitk
        Match(title="Confirmation"),      # tastyworks exit box
        Match(title="Qalculate!"),        # qalculate-gtk
        Match(title="pinentry"),          # GPG key password entry
        Match(title="tastycharts"),       # tastytrade pop-out charts
        Match(title="tastytrade"),        # tastytrade pop-out side gutter
        Match(title="tastytrade - Portfolio Report"), # tastytrade pop-out allocation
        Match(wm_class="tasty.javafx.launcher.LauncherFxApp"), # tastytrade settings
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = False

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/scripts/autostart.sh"])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
