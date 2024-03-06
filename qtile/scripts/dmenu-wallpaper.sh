#!/bin/bash

main()
{
    local choice=$(ls ~/.config/qtile/wallpapers/ | $DMENU $DMENU_WIDTH 'Wallpapers:')
    if [[ -n $choice && $(echo -e "No\nYes" | $DMENU $DMENU_WIDTH "Choose \"$choice\"?") = "Yes" ]]
    then
        feh --bg-fill ~/.config/qtile/wallpapers/$choice
        notify-send "\"$choice\" is your new wallpaper"
    else
        exit 1
    fi
}

main