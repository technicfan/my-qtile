#!/bin/sh

function shown()
{
    cd ~/.config/qtile/mpris
    touch 1 && rm 0
}

function hidden()
{
    cd ~/.config/qtile/mpris
    touch 0 && rm 1
}

case $1 in
"mpris")
    case $2 in
    "toggle")
        qtile cmd-obj -o widget mpris -f toggle
        if cat ~/.config/qtile/mpris/0
        then
            shown
        elif cat ~/.config/qtile/mpris/1
        then
            hidden
        fi
        ;;
    "show")
        if cat ~/.config/qtile/mpris/0
        then
            qtile cmd-obj -o widget mpris -f toggle
        fi
        shown
        ;;
    "hide")
        if cat ~/.config/qtile/mpris/1
        then
            qtile cmd-obj -o widget mpris -f toggle
        fi
        hidden
        ;;
    "restore")
        if cat ~/.config/qtile/mpris/1
        then
            qtile cmd-obj -o widget mpris -f toggle
        fi
        ;;
    "shown")
        shown
        ;;
    "hidden")
        hidden
        ;;
    *)
        exit 1
    esac
    ;;
"systray")
    case $2 in
    "toggle")
        if cat ~/.config/qtile/mpris/1
        then
            qtile cmd-obj -o widget mpris -f toggle &
            qtile cmd-obj -o widget widgetbox -f toggle
        else
            qtile cmd-obj -o widget widgetbox -f toggle
        fi
        ;;
    *)
        exit 1
    esac
    ;;
*)
    exit 1
esac