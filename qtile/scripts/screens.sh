#!/bin/bash

check()
{
    # had to use full path because it needs to be run by root for sddm xscreen config
    echo "$(awk -F " = " '/screen_state/ {print $2}' /home/technicfan/.config/qtile/states/states.ini)"
}

set_state()
{
    if ! [[ $(check) = "$1" ]]
    then
        sed -i "s/screen_state = .*/screen_state = $1/g" ~/.config/qtile/states/states.ini
    fi
}

one()
{
    if [[ $XDG_SESSION_TYPE = "wayland" ]]
    then
        one-wlr
    else
        xrandr --output HDMI-0 --off --output DP-4 --auto --primary
    fi
}

two()
{
    xrandr --output HDMI-0 --auto --primary --output DP-4 --off
}

both()
{
    if [[ $XDG_SESSION_TYPE = "wayland" ]]
    then
        both-wlr
    else
        xrandr --output DP-4 --auto --primary --output HDMI-0 --auto --right-of DP-4
    fi
}

mirror()
{
    xrandr --output DP-4 --auto --primary --output HDMI-0 --auto --same-as DP-4
}

one-wlr()
{
    wlr-randr --output HDMI-A-1 --off --output DP-3 --mode 1920x1080 --preferred
}

two-wlr()
{
    xrandr --output HDMI-0 --on  --primary --output DP-4 --off
}

both-wlr()
{
    wlr-randr --output DP-3 --mode 1920x1080 --preferred --output HDMI-A-1 --on --mode 1920x1080 --pos 1920, 0
}

mirror-wlr()
{
    echo "nix"
}


main()
{
    case $1 in
    "one")
        $1
        set_state 1
        ;;
    "two")
        $1
        set_state 2
        ;;
    "both")
        $1
        wallpaper
        set_state 3
        ;;
    "mirror")
        $1
        set_state 4
        ;;
    "off")
        xrandr --output HDMI-0 --off --output DP-4 --off
        ;;
    "restore")
        case $(check) in
        "1")
            one
            ;;
        "2")
            two
            ;;
        "3")
            both
            ;;
        "4")
            mirror
        esac
        ;;
    *)
        exit 1
    esac
}

main $1 $2