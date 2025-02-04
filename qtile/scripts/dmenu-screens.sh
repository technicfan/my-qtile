#!/bin/bash

main()
{
    connected="$(xrandr | grep -w 'connected')"
    declare -a outputs
    primary="$(grep -w 'primary' <<< "$connected" | awk '{ print $1 }')"
    if [[ -n "$primary" ]]
    then
        outputs+=( "$primary (primary)" )
        outputs+=( "$(grep -vw 'primary' <<< "$connected" | awk '{ print $1 }')" )
    else
        primary="$(awk 'NR==1{ print $1 }' <<< "$connected")"
        outputs+=( "$primary (primary)" )
        outputs+=( "$(grep -vw 'primary' <<< "$connected" | awk 'NR>1{ print $1 }')" )
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
                    xrandr --output "$(awk '{ print $1 }' <<< "${outputs[i]}")" --primary --auto
                else
                    xrandr --output "${outputs[i]}" --auto --"${choice//all-/}"-of "$(awk '{ print $1 }' <<< "${outputs[$(( i-1 ))]}")"
                fi
            done
            ;;
        "mirror")
            for i in "${!outputs[@]}"
            do
                if [[ "${outputs[i]}" =~ ^.*\(primary\)$ ]]
                then
                    xrandr --output "$(awk '{ print $1 }' <<< "${outputs[i]}")" --primary --auto
                else
                    xrandr --output "$(awk '{ print $1 }' <<< "${outputs[i]}")" --auto --same-as "$primary"
                fi
            done
            ;;
        "off")
            for i in "${!outputs[@]}"
            do
                xrandr --output "$(awk '{ print $1 }' <<< "${outputs[i]}")" --off
            done
            ;;
        *)
            for i in "${!outputs[@]}"
            do
                if [[ "${outputs[i]}" = "$choice" ]]
                then
                    xrandr --output "$(awk '{ print $1 }' <<< "$choice")" --primary --auto
                else
                    xrandr --output "$(awk '{ print $1 }' <<< "${outputs[i]}")" --off
                fi
            done
            ;;
        esac
    fi
}

main
