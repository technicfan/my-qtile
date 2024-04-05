#!/bin/bash

main()
{
    local selected="$(ps -u $USER -f | grep -v PID | awk '{print $2" - "$5" - "$8}' | $DMENU "Kill process:" | awk '{print $1" "$5}')"

    if [[ -n $selected ]]
    then
        if [[ $(echo -e "No\nYes" | $DMENU "Kill $(echo $selected | awk '{print $2}')?") == "Yes" ]]
        then
            kill "$(echo $selected | awk -F " " '{ print $1 }')"
            exit 0
        else
            exit 1
        fi
    fi
}

main
