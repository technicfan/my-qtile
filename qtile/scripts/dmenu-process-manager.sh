#!/bin/bash

main()
{
    local DMENU_WIDTH=" -z 960 -p"

    local selected="PID CMD"

    while [[ $selected = "PID CMD" ]]
    do
        local selected="$(ps --user "$USER" -F | $DMENU $DMENU_WIDTH "Kill process:" | awk '{print $2" "$11}')"
    done

    echo $(echo $selected | awk -F " " '{ print $1 }')

    if [[ -n $selected ]]
    then
        if [[ $(echo -e "No\nYes" | $DMENU $DMENU_WIDTH  "Kill $selected?") == "Yes" ]]
        then
            kill "$(echo $selected | awk -F " " '{ print $1 }')"
            exit 0
        else
            exit 1
        fi
    fi
}

main
