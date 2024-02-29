#!/bin/bash

main()
{
    local options=(
        "Monitor 1"
        "Monitor 2"
        "Both Monitors"
        "Mirror"
        "Off"
    )

    local choice=$(printf '%s\n' "${options[@]}" | $DMENU $DMENU_WIDTH 'Monitors:')

    case $choice in
    "Monitor 1")
        ~/.config/qtile/scripts/screens.sh one
        ;;
    "Monitor 2")
        ~/.config/qtile/scripts/screens.sh two
        ;;
    "Both Monitors")
        ~/.config/qtile/scripts/screens.sh both
        ;;
    "Mirror")
        ~/.config/qtile/scripts/screens.sh mirror
        ;;
    "Off")
        ~/.config/qtile/scripts/screens.sh off
        ;;
    *)
        exit 0
    esac
}

main
