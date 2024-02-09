#!/bin/sh

function wallpaper()
{
    # Arcolinux
    feh --bg-fill ".config/qtile/wallpapers/Arcolinux-text-dark-rounded-1080p.png"

    # other:
    # Arcolinux-text-dark-rounded-1080p.png
    # Archlinux-text-dark-rounded-1080p.png
    # linux.png
    # retro-arco.png
    #feh --bg-fill "path/to/wallpaper"
}

if [ $1 = "one" ]
then
    xrandr --output HDMI-0 --off --output DP-4 --auto
    cd .config/qtile/screens
    touch 1 && rm 2
elif [ $1 = "two" ]
then
    xrandr --output DP-4 --auto --output HDMI-0 --auto --right-of DP-4
    wallpaper
    cd .config/qtile/screens
    touch 2 && rm 1
elif [ $1 = "restore" ]
then
    if cat ~/.config/qtile/screens/1
    then
        xrandr --output HDMI-0 --off --output DP-4 --auto
    elif cat ~/.config/qtile/screens/2
    then
        xrandr --output DP-4 --auto --output HDMI-0 --auto --right-of DP-4
    fi
elif [ $1 = "wallpaper" ]
then
    if [ -z $2 ]
    then
        wallpaper
    else
        feh --bg-fill $2
    fi
fi