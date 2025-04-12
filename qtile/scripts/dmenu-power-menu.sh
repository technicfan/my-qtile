#!/bin/bash

main()
{
    locker="i3lock-fancy"

    options=(
        "Lock"
        "Logout"
        "Reboot"
        "Shutdown"
        "Suspend"
    )

    choice=$(printf '%s\n' "${options[@]}" | $DMENU 'Power menu:')

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
        choice=$(echo -e "System\nBIOS\nWindows" | $DMENU 'Reboot destination:')
        if [[ $choice =~ System|BIOS|Windows && "$(echo -e "No\nYes" | $DMENU "Reboot to ${choice}?")" == "Yes" ]]
        then
            case $choice in
            "System")
                systemctl reboot
            ;;
            "BIOS")
                systemctl reboot --firmware-setup
                ;;
            "Windows")
                systemctl reboot --boot-loader-entry=windows.conf
                ;;
            *)
                exit 0
                ;;
            esac
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
