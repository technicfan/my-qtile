#!/bin/bash

main()
{
    local locker="i3lock-fancy-dualmonitor"

    local options=(
        "Lock"
        "Logout"
        "Reboot"
        "Shutdown"
        "Suspend"
    )

    local choice=$(printf '%s\n' "${options[@]}" | $DMENU 'Power menu:')

    case $choice in
    "Lock")
        $locker
        ;;
    "Logout")
        if [[ "$(echo -e "No\nYes" | $DMENU "${choice}?")" == "Yes" ]]
        then
            qtile cmd-obj -o cmd -f shutdown
        else
            exit 0
        fi
        ;;
    "Reboot")
        if [[ "$(echo -e "No\nYes" | $DMENU "${choice}?")" == "Yes" ]]
        then
            systemctl reboot
        else
            exit 0
        fi
        ;;
    "Shutdown")
        if [[ "$(echo -e "No\nYes" | $DMENU "${choice}?")" == "Yes" ]]
        then
            systemctl poweroff
        else
            exit 0
        fi
        ;;
    "Suspend")
        if [[ "$(echo -e "No\nYes" | $DMENU "${choice}?")" == "Yes" ]]
        then
            systemctl suspend
        else
            exit 0
        fi
        ;;
    *)
        exit 0
    esac
}

main
