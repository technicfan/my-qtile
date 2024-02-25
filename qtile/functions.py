from libqtile import qtile
from libqtile.lazy import lazy

# A function for hide/show all the windows in a group
@lazy.function
def minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()

# Window names
def ReplaceWindowName(text): 
    if text == "Windows 11 [wird ausgeführt] - Oracle VM VirtualBox" or text == "Windows 11 [ausgeschaltet] - Oracle VM VirtualBox" or text == "Windows 11 [wird ausgeschaltet] - Oracle VM VirtualBox":
        text = "Windows 11"
    elif text == "Windows 7 [wird ausgeführt] - Oracle VM VirtualBox" or text == "Windows 7 [ausgeschaltet] - Oracle VM VirtualBox" or text == "Windows 7 [wird ausgeschaltet] - Oracle VM VirtualBox":
        text = "Windows 7"
    else:
        text = text
    return text