#!/bin/sh

wallpaper()
{
    feh --bg-fill ".config/qtile/wallpapers/communism2.png"
}

one()
{
    xrandr --output HDMI-0 --off --output DP-4 --auto
}

two()
{
    xrandr --output HDMI-0 --auto --output DP-4 --off
}

both()
{
    xrandr --output DP-4 --auto --output HDMI-0 --auto --right-of DP-4
}

mirror()
{
    xrandr --output DP-4 --auto --output HDMI-0 --auto --same-as DP-4
}


main()
{
    case $1 in
    "one")
        $1
        cd .config/qtile/screens
        touch 1 && rm 2; rm 3; rm 4
        ;;
    "two")
        $1
        cd .config/qtile/screens
        touch 2 && rm 1; rm 3; rm 4
        ;;
    "both")
        $1
        wallpaper
        cd .config/qtile/screens
        touch 3 && rm 1; rm 2; rm 4
        ;;
    "mirror")
        $1
        cd .config/qtile/screens
        touch 4 && rm 1; rm 2; rm 3
        ;;
    "off")
        xrandr --output HDMI-0 --off --output DP-4 --off
        ;;
    "restore")
        if cat .config/qtile/screens/1
        then
            one
        elif cat .config/qtile/screens/2
        then
            two
        elif cat .config/qtile/screens/3
        then
            both
        elif cat .config/qtile/screens/4
        then
            mirror
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
}

main $1 $2