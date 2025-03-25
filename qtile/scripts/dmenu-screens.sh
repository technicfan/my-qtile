#!/bin/bash

main()
{
    if [[ $XDG_SESSION_TYPE = "wayland" ]]
    then
        randr="wlr-randr"
        primary_display="preferred"
        connected="$(wlr-randr | grep -v '^ ')"
    else
        randr="xrandr"
        primary_display="primary"
        connected="$(xrandr | grep -w 'connected')"
    fi

    declare -a outputs
    primary="$(grep -w 'primary' <<< "$connected" | awk '{ print $1 }')"
    if [[ -n "$primary" ]]
    then
        outputs+=( "$primary (primary)" )
        outputs+=( "$(grep -vw 'primary' <<< "$connected" | awk '{ print $1 }')" )
    else
        primary="$(awk 'NR==1{ print $1 }' <<< "$connected")"
        outputs+=( "$(grep -vw 'primary' <<< "$connected" | awk '{ print $1 }')" )
    fi
    options=( "all-right" "all-left" "mirror" "off" )

    choice=$(printf '%s\n' "${outputs[@]}" "${options[@]}" | $DMENU 'Monitors:')

    if [[ -n "$choice" ]]
    then
        case "$choice" in
        "all"*)
            for i in "${!outputs[@]}"
            do
                if [[ "${outputs[i]}" =~ ^.*\(primary\)$ ]]
                then
                    "$randr" --output "$(awk '{ print $1 }' <<< "${outputs[i]}")" --"$primary_display" --mode 1920x1080
                else
                    "$randr" --output "${outputs[i]}" --mode 1920x1080 --"${choice//all-/}"-of "$(awk '{ print $1 }' <<< "${outputs[$(( i-1 ))]}")"
                fi
            done
            ;;
        "mirror")
            for i in "${!outputs[@]}"
            do
                if [[ "${outputs[i]}" =~ ^.*\(primary\)$ ]]
                then
                    "$randr" --output "$(awk '{ print $1 }' <<< "${outputs[i]}")" --"$primary_display" --mode 1920x1080
                else
                    "$randr" --output "$(awk '{ print $1 }' <<< "${outputs[i]}")" --mode 1920x1080 --same-as "$primary"
                fi
            done
            ;;
        "off")
            for i in "${!outputs[@]}"
            do
                "$randr" --output "$(awk '{ print $1 }' <<< "${outputs[i]}")" --off
            done
            ;;
        *)
            for i in "${!outputs[@]}"
            do
                if [[ "${outputs[i]}" = "$choice" ]]
                then
                    $randr --output "$(awk '{ print $1 }' <<< "$choice")" --$primary_display --mode 1920x1080
                else
                    $randr --output "$(awk '{ print $1 }' <<< "${outputs[i]}")" --off
                fi
            done
            ;;
        esac
    fi
}

main
