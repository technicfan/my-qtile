#!/bin/sh

shown()
{
    cd ~/.config/qtile/$1
    touch 1 && rm 0
}

hidden()
{
    cd ~/.config/qtile/$1
    touch 0 && rm 1
}

open_query()
{
    if cat ~/.config/qtile/$1/0
    then
        exit 1
    elif cat ~/.config/qtile/$1/1
    then
        exit 0
    fi
}

case $1 in
"mpris")
    case $2 in
    "toggle")
        if cat ~/.config/qtile/systray/0
        then
            qtile cmd-obj -o widget mpris -f toggle
            if cat ~/.config/qtile/$1/0
            then
                shown $1
            elif cat ~/.config/qtile/$1/1
            then
                hidden $1
            fi
        fi
        ;;
    "show")
        if cat ~/.config/qtile/systray/0
        then
            qtile cmd-obj -o widget mpris -f open
        fi
        shown $1
        ;;
    "hide")
        if cat ~/.config/qtile/systray/0
        then
            qtile cmd-obj -o widget mpris -f close
        fi
        hidden $1
        ;;
    "restore")
        if cat ~/.config/qtile/mpris/1
        then
            qtile cmd-obj -o widget mpris -f open
        fi
        ;;
    "shown")
        shown $1
        ;;
    "hidden")
        hidden $1
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
        fi

        qtile cmd-obj -o widget widgetbox -f toggle
        if cat ~/.config/qtile/$1/0
        then
            shown $1
        elif cat ~/.config/qtile/$1/1
        then
            hidden $1
        fi
        ;;
    "shown")
        shown $1
        ;;
    "hidden")
        hidden $1
        ;;
    *)
        exit 1
    esac
    ;;
*)
    exit 1
esac