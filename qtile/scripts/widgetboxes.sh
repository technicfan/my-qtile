#!/bin/sh

function shown()
{
    cd ~/.config/qtile/mpris
    touch 1 && rm 0
    cd -
}

function hidden()
{
    cd ~/.config/qtile/mpris
    touch 0 && rm 1
    cd -
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
        qtile cmd-obj -o widget mpris -f open
        shown
        ;;
    "hide")
        qtile cmd-obj -o widget mpris -f close
        hidden
        ;;
    "restore")
        if cat ~/.config/qtile/mpris/1
        then
            qtile cmd-obj -o widget mpris -f open
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