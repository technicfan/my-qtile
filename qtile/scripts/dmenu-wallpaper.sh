#!/bin/bash

revert()
{
    feh --bg-fill "$2/$1"
    name=$(sed 's/.*\///g' <<< "$1")
    if [[ -n $name ]]
    then
        notify-send "reverted to \"$name\""
    else
        notify-send "reverted to \"$1\""
    fi
}

main()
{
    dir="$HOME/.config/qtile/wallpapers"
    default="more/own/antifa.png"

    if [[ $1 = "print" ]]
    then
        echo "$dir/$default"
        return
    fi

    choice=$(printf '%s\n' "Revert to default" "$(find -L ~/.config/qtile/wallpapers -type f | sed "s|$dir/||g")" | $DMENU  'Wallpapers:')
    if [[ $choice = "Revert to default" ]]
    then
        revert "$default" "$dir"
    elif [[ -n $choice ]]
    then
        feh --bg-fill "$dir/$choice"
        notify-send "\"$(awk -F "/" '{print $NF}' <<< "$choice")\" is your new wallpaper"

        if [[ "$default" != "$choice" ]]
        then
            choice2=$(echo -e "No\nRevert to default\nYes" | $DMENU "Set \"$choice\" as default?")
            if [[ $choice2 = "Yes" ]]
            then
                sed -i "s|default=\".*\"|default=\"$choice\"|" ~/.config/qtile/scripts/dmenu-wallpaper.sh && \
                notify-send "\"$(awk -F "/" '{print $NF}' <<< "$choice")\" is your new default"
            elif [[ $choice2 = "Revert to default" ]]
            then
                revert "$default" "$dir"
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

main "$@"