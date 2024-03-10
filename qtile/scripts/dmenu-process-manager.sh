#!/bin/bash

main()
{
    local DMENU_POS="-l 20 -z 928 -p"

    local selected="PID CMD"

    while [[ $selected = "PID CMD" ]]
    do
        local selected="$(ps -u $USER -f | $DMENU $DMENU_POS "Kill process:" | awk '{print $2" "$8}')"
    done

    echo $(echo $selected | awk -F " " '{ print $1 }')

    if [[ -n $selected ]]
    then
        if [[ $(echo -e "No\nYes" | $DMENU $DMENU_POS  "Kill $selected?") == "Yes" ]]
        then
            kill "$(echo $selected | awk -F " " '{ print $1 }')"
            exit 0
        else
            exit 1
        fi
    fi
}

main
