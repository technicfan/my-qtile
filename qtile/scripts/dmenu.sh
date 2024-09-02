#!/bin/bash

load()
{
    cd ~/.config/qtile/scripts || exit 1
    export DMENU="dmenu -i -p"
}

load_noi()
{
    cd ~/.config/qtile/scripts || exit 1
    export DMENU="dmenu -i -noi -p"
}

main()
{
    case $1 in
    "kill")
        load
        ./dmenu-process-manager.sh
        ;;
    "output-switcher")
        load_noi
        ./dmenu-${1}.sh
        ;;
    "logout")
        load_noi
        ./dmenu-power-menu.sh
        ;;
    "unicode")
        load
        ./dmenu-${1}.sh
        ;;
    "screens")
        load_noi
        ./dmenu-${1}.sh
        ;;
    "vms")
        load
        ./dmenu-${1}.sh
        ;;
    "icon-color")
        load
        ./dmenu-${1}.sh
        ;;
    "wallpaper")
        load
        ./dmenu-${1}.sh 
        ;;   
    "git-repos")
        load
        ./dmenu-${1}.sh
        ;;
    "clear-clipcat")
        load_noi
        if [[ "$(echo -e "No\nYes" | $DMENU "Clear Clipboard History?")" == "Yes" ]]
        then
            clipcatctl clear
        fi
        ;;
    "dmenu")
        load
        if [[ -n $2 ]]
        then
            $DMENU "$2"
        else
            exit 1
        fi
        ;;
    *)
        exit 1
    esac
}

main $1 $2