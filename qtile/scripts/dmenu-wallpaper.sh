#!/bin/bash

main()
{
    local DMENU_WIDTH=" -z 450 -p"

    local choice=$(ls ~/.config/qtile/wallpapers/ | $DMENU $DMENU_WIDTH 'Wallpapers:')
    if [[ -n $choice && $(echo -e "No\nYes" | $DMENU $DMENU_WIDTH "Choose \"$choice\"?") = "Yes" ]]
    then
        feh --bg-fill "$(echo ~)/.config/qtile/wallpapers/$choice"
        notify-send "\"$choice\" is your new wallpaper"

        local default=$(cat ~/.config/qtile/scripts/screens.sh | awk -F "/" '/wallpapers/ {print $5}' | awk -F "\"" '{print $1}')
        if [[ -n $default && $default != $choice ]]
        then
            local choice2=$(echo -e "No\nYes\nRevert to default" | $DMENU $DMENU_WIDTH "Set \"$choice\" as default?")
            if [[ -n $choice2 && $choice2 = "Yes" ]]
            then
                sed -i "s/wallpapers\/.*/wallpapers\/$choice\"/g" ~/.config/qtile/scripts/screens.sh
                notify-send "\"$choice\" is your new default"
            elif [[ $choice2 = "Revert to default" ]]
            then
                ~/.config/qtile/scripts/screens.sh wallpaper
                notify-send "reverted to \"$default\""
            else
                exit 1
            fi
        else
            exit 1
        fi
    else
        exit 1
    fi
}

main