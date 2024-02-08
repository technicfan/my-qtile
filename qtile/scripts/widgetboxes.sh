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

if [ $1 = "mpris" ]
then
    if [ $2 = "toggle" ]
    then
        qtile cmd-obj -o widget mpris -f toggle
        if cat ~/.config/qtile/mpris/0
        then
            shown
        elif cat ~/.config/qtile/mpris/1
        then
            hidden
        fi
        elif [ $2 = "show" ]
        then
        if cat ~/.config/qtile/mpris/0
        then
            qtile cmd-obj -o widget mpris -f toggle
        fi
        shown
    elif [ $2 = "hide" ]
    then
        if cat ~/.config/qtile/mpris/1
        then
            qtile cmd-obj -o widget mpris -f toggle
        fi
        hidden
    elif [ $2 = "restore" ]
    then
        if cat ~/.config/qtile/mpris/1
        then
            qtile cmd-obj -o widget mpris -f toggle
        fi
    elif [ $2 = "shown" ]
    then
        shown
    elif [ $2 = "hidden" ]
    then
        hidden
    fi
elif [ $1 = "systray" ]
then
    if [ $2 = "toggle" ]
    then
        if cat ~/.config/qtile/mpris/1
        then
            qtile cmd-obj -o widget mpris -f toggle &
            qtile cmd-obj -o widget widgetbox -f toggle
        else
            qtile cmd-obj -o widget widgetbox -f toggle
        fi
    fi
fi