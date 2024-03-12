#!/bin/bash

revert()
{
    ~/.config/qtile/scripts/screens.sh wallpaper
    notify-send "reverted to \"$1\""
}

main()
{
    for i in $(seq 1 $(ls -1 ~/.config/qtile/wallpapers | wc -l))
    do
        local wallpapers[$i]=$(ls -m ~/.config/qtile/wallpapers/ | awk -F ", " '{ print $(shell_var='"$i"') }' )
    done
    local default=$(cat ~/.config/qtile/scripts/screens.sh | awk -F "/" '/wallpapers/ {print $5}' | awk -F "\"" '{print $1}')

    local choice=$(printf '%s\n' "Revert to default" "${wallpapers[@]}" | $DMENU $DMENU_POS 'Wallpapers:')

    if [[ $choice = "Revert to default" ]]
    then
        revert $default
    elif [[ -n $choice && $(echo -e "No\nYes" | $DMENU $DMENU_POS "Choose \"$choice\"?") = "Yes" ]]
    then
        feh --bg-fill "$(echo ~)/.config/qtile/wallpapers/$choice"
        notify-send "\"$choice\" is your new wallpaper"

        if [[ -n $default && $default != $choice ]]
        then
            local choice2=$(echo -e "No\nYes\nRevert to default" | $DMENU $DMENU_POS "Set \"$choice\" as default?")
            if [[ -n $choice2 && $choice2 = "Yes" ]]
            then
                sed -i "s/wallpapers\/.*/wallpapers\/$choice\"/g" ~/.config/qtile/scripts/screens.sh
                notify-send "\"$choice\" is your new default"
            elif [[ $choice2 = "Revert to default" ]]
            then
                revert $default
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