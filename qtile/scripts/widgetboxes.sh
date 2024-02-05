#!/bin/sh

if [ $1 = "mpris" ]
then
    qtile cmd-obj -o widget mpris -f toggle
    if cat ~/.config/qtile/mpris/0
    then
        cd ~/.config/qtile/mpris
        touch 1 && rm 0
    elif cat ~/.config/qtile/mpris/1
    then
        cd ~/.config/qtile/mpris
        touch 0 && rm 1
    fi
elif [ $1 = "systray" ]
then
    if cat ~/.config/qtile/mpris/1
    then
        qtile cmd-obj -o widget mpris -f toggle &
        qtile cmd-obj -o widget widgetbox -f toggle
    else
        qtile cmd-obj -o widget widgetbox -f toggle
    fi
elif [ $1 = "reset" ]
then
    cd ~/.config/qtile/mpris
    touch 0 && rm 1
elif [ $1 = "fix" ]
then
    cd ~/.config/qtile/mpris
    touch 1 && rm 0
fi