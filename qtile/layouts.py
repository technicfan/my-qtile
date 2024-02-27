# ____  _____ ____ _____ ____   _____   __   ____    _    ____ ___ _____  _    _     ___ ____  __  __   _
#|  _ \| ____/ ___|_   _|  _ \ / _ \ \ / /  / ___|  / \  |  _ \_ _|_   _|/ \  | |   |_ _/ ___||  \/  | | |
#| | | |  _| \___ \ | | | |_) | | | \ V /  | |     / _ \ | |_) | |  | | / _ \ | |    | |\___ \| |\/| | | |
#| |_| | |___ ___) || | |  _ <| |_| || |   | |___ / ___ \|  __/| |  | |/ ___ \| |___ | | ___) | |  | | |_|
#|____/|_____|____/ |_| |_| \_\\___/ |_|    \____/_/   \_\_|  |___| |_/_/   \_\_____|___|____/|_|  |_| (_)

from libqtile import layout
from libqtile.config import Match

from colors import colors

### LAYOUTS ###
layouts = [
    layout.Spiral(
        main_pane = "left",
        clockwise = True,
        new_client_position = "after_current",
        ratio = 0.5,
        ratio_increment = 0,
        border_width = 2,
        margin = [4, 8, 8, 8],
        border_focus = colors[1],
        border_normal = colors[3]
    ),
    layout.Max(),
]

floating_layout = layout.Floating(
    border_focus=colors[1],
    border_normal=colors[3],
    border_width=2,
    float_rules=[
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
        Match(wm_class="delphi32.exe"), # Delphi 7 IDE
        Match(wm_class="quickgui"), # quickemu gui vm manger
    ]
)