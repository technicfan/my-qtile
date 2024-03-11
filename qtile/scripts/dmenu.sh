#!/bin/bash

load()
{
    cd ~/.config/qtile/scripts
    export DMENU="dmenu -i -nb #282828 -nf #d3869b -sb #dfbf8e -sf #282828 -fn 'JetBrains:bold:pixelsize=12' -x 8 -y 8 -bw 2"
    export DMENU_POS=" -z 1900 -h 24 -p"
}

main()
{
    case $1 in
    "kill")
        load
        ./dmenu-process-manager.sh
        ;;
    "output-switcher")
        load
        ./dmenu-${1}.sh
        ;;
    "logout")
        load
        ./dmenu-power-menu.sh
        ;;
    # stolen from Luke Smith
    "unicode")
        load
        ./dmenu-${1}.sh
        ;;
    # own
    "screens")
        load
        ./dmenu-${1}.sh
        ;;
    "wine_vm")
        load
        ./dmenu-${1}.sh
        ;;
    "icon-color")
        load
        ./dmenu-${1}.sh dmenu
        ;;
    "wallpaper")
        load
        ./dmenu-${1}.sh 
        ;;   
    "dmenu")
        load
        if [[ -n $2 ]]
        then
            $DMENU$DMENU_POS "$2"
        else
            exit 1
        fi
        ;;
    *)
        exit 1
    esac
}

main $1 $2