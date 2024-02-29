#!/bin/bash

# technicfan
#dmenu="dmenu -i -l 20 -nb #133912 -nf #87a757 -sb #87a757 -sf #133912 -fn 'JetBrains:bold:pixelsize=14'"

load()
{
    cd ~/.config/qtile/scripts
    export DMENU="dmenu -i -l 20 -nb #282828 -nf #dfbf8e -sb #dfbf8e -sf #282828 -fn 'JetBrains:bold:pixelsize=14'"
    export DMENU_WIDTH=" -z 300 -p"
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
    "monitor")
        load
        ./dmenu-${1}.sh
        ;;
    "wine_vm")
        load
        ./dmenu-${1}.sh
        ;;
    "dmenu")
        load
        if [[ -n $2 ]]
        then
            $DMENU$DMENU_WIDTH "$2"
        else
            exit 1
        fi
        ;;
    *)
        exit 1
    esac
}

main $1 $2