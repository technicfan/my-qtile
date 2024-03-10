#!/bin/bash

main()
{
    local DMENU_WIDTH=" -z 400 -p"

    local choice=$(ls ~/.config/qtile/wallpapers/ | $DMENU $DMENU_WIDTH 'Wallpapers:')
    if [[ -n $choice && $(echo -e "No\nYes" | $DMENU $DMENU_WIDTH "Choose \"$choice\"?") = "Yes" ]]
    then
        feh --bg-fill ~/.config/qtile/wallpapers/$choice
        notify-send "\"$choice\" is your new wallpaper"

        if [[ $(echo -e "No\nYes" | $DMENU $DMENU_WIDTH "Set \"$choice\" as default?") = "Yes" ]]
        then
            sed -i "s/wallpapers\/.*/wallpapers\/$choice\"/g" ~/.config/qtile/scripts/screens.sh
            notify-send "\"$choice\" is your new default"
        else
            exit 1
        fi
    else
        exit 1
    fi
}

main