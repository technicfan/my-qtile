#!/bin/sh

if [ $1 = "one" ]
then
    xrandr --output HDMI-0 --off --output DP-4 --auto
    cd ~/.config/qtile/screens
    touch 1 && rm 2
elif [ $1 = "two" ]
then
    xrandr --output DP-4 --auto --output HDMI-0 --auto --right-of DP-4
    cd ~/.config/qtile/screens
    touch 2 && rm 1

    # Arcolinux-text-dark-rounded-1080p.png
    # Archlinux-text-dark-rounded-1080p.png
    # linux.png
    # retro-arco.png

    # Arcolinux
    feh --bg-fill "~/.config/qtile/wallpapers/Arcolinux-text-dark-rounded-1080p.png" &

    # other
    #feh --bg-fill "path/to/wallpaper" &
else
    exit
fi