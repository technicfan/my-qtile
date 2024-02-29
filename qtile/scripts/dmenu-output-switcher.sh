#!/bin/bash

main()
{
    local DMENU_WIDTH=" -z 400 -p"

    get_default_sink() {
        pactl --format=json info | jq -r .default_sink_name
    }

    get_all_sinks() {
        pactl --format=json list short sinks \
            | current=$(get_default_sink) jq -r '.[] | if .name == env.current then .state="* " else .state="" end | .state + .name'
    }

    local choice=$(printf '%s\n' "$(get_all_sinks)" | sort | $DMENU $DMENU_WIDTH 'Sink:') || exit 1

    if [ "$choice" ]
    then
        if [[ "${choice}" == "* $(get_default_sink)" ]]
        then
        exit 0
        fi
        pactl set-default-sink "${choice}"
    else
        exit 0
    fi
}

main
