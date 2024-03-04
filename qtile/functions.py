# ____  _____ ____ _____ ____   _____   __   ____    _    ____ ___ _____  _    _     ___ ____  __  __   _
#|  _ \| ____/ ___|_   _|  _ \ / _ \ \ / /  / ___|  / \  |  _ \_ _|_   _|/ \  | |   |_ _/ ___||  \/  | | |
#| | | |  _| \___ \ | | | |_) | | | \ V /  | |     / _ \ | |_) | |  | | / _ \ | |    | |\___ \| |\/| | | |
#| |_| | |___ ___) || | |  _ <| |_| || |   | |___ / ___ \|  __/| |  | |/ ___ \| |___ | | ___) | |  | | |_|
#|____/|_____|____/ |_| |_| \_\\___/ |_|    \____/_/   \_\_|  |___| |_/_/   \_\_____|___|____/|_|  |_| (_)

from libqtile.lazy import lazy

# A function for hide/show all the windows in a group
@lazy.function
def minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()