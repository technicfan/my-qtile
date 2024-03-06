#!/bin/bash

toggle()
{
    numlockx toggle
}

set_rgb()
{
    case $(xset -q | awk -F ":" '/Num Lock:/ { print $5 }' | awk -F " " '{ print $1 }') in
    "on")
        polychromatic-cli -e keyboard-numpad
        ;;
    "off")
        polychromatic-cli -e keyboard
        ;;
    *)
        exit 1
    esac
}

main()
{
    if [[ -n $1 ]]
    then
        if [[ $1 = "toggle" ]]
        then
            toggle
            set_rgb
        elif [[ $1 = "match" ]]
        then
            set_rgb
        fi
    else
        exit 1
    fi
}

main $1