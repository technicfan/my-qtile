#!/bin/sh

function wallpaper()
{
    feh --bg-fill ".config/qtile/wallpapers/enterprise.png"
}

case $1 in
"one")
    xrandr --output HDMI-0 --off --output DP-4 --auto
    cd .config/qtile/screens
    touch 1 && rm 2
    cd -
    ;;
"two")
    xrandr --output DP-4 --auto --output HDMI-0 --auto --right-of DP-4
    wallpaper
    cd .config/qtile/screens
    touch 2 && rm 1
    cd -
    ;;
"restore")
    if cat .config/qtile/screens/1
    then
        xrandr --output HDMI-0 --off --output DP-4 --auto
    elif cat .config/qtile/screens/2
    then
        xrandr --output DP-4 --auto --output HDMI-0 --auto --right-of DP-4
    fi
    ;;
"wallpaper")
    if [ -z $2 ]
    then
        wallpaper
    else
        feh --bg-fill $2
    fi
    ;;
*)
    exit 1
esac