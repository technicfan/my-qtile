#!/bin/bash

dmenu="dmenu -i -l 20 -nb #133912 -nf #87a757 -sb #87a757 -sf #133912 -fn 'JetBrains:bold:pixelsize=14'"
dmenu_width=" -z 300 -p"
locker="i3lock-fancy-dualmonitor"

if [ $1 = "kill" ]
then
    dmenu_width=" -z 960 -p"

    selected="$(ps --user "$USER" -F \
            | $dmenu $dmenu_width "Kill process:" \
            | awk '{print $2" "$11}')"

    if [[ -n $selected ]]
    then
        answer="$(echo -e "No\nYes" | $dmenu $dmenu_width  "Kill $selected?")"

        if [[ $answer == "Yes" ]]
        then
            kill -9 "${selected%% *}"
            exit 0
        else
            exit 1
        fi
    fi
elif [ $1 = "output-switcher" ]
then
    dmenu_width=" -z 400 -p"

    get_default_sink() {
        pactl --format=json info | jq -r .default_sink_name
    }

    get_all_sinks() {
        pactl --format=json list short sinks \
            | current=$(get_default_sink) jq -r '.[] | if .name == env.current then .state="* " else .state="" end | .state + .name'
    }

    choice=$(printf '%s\n' "$(get_all_sinks)" \
        | sort \
        | $dmenu $dmenu_width 'Sink: ') || exit 1

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
elif [ $1 = "logout" ]
then
    declare -a options=(
        "Sperren"
        "Abmelden"
        "Neustarten"
        "Herunterfahren"
        "Bereitschaft"
    )

    declare -a managers
    while IFS= read -r manager
    do
        managers+=("${manager,,}")
    done < <(uname)

    choice=$(printf '%s\n' "${options[@]}" | $dmenu $dmenu_width 'Power menu:')

    case $choice in
    'Abmelden')
        if [[ "$(echo -e "No\nYes" | $dmenu $dmenu_width "${choice}?")" == "Yes" ]]
        then
            for manager in "${managers[@]}"; do
                loginctl kill-user "$UID"
            done
        else
            exit 1
        fi
        ;;
    'Sperren')
        ${locker}
        ;;
    'Neustarten')
        if [[ "$(echo -e "No\nYes" | $dmenu $dmenu_width "${choice}?")" == "Yes" ]]
        then
            systemctl reboot
        else
            exit 0
        fi
        ;;
    'Herunterfahren')
        if [[ "$(echo -e "No\nYes" | $dmenu $dmenu_width "${choice}?")" == "Yes" ]]
        then
            systemctl poweroff
        else
            exit 0
        fi
        ;;
    'Bereitschaft')
        if [[ "$(echo -e "No\nYes" | $dmenu $dmenu_width "${choice}?")" == "Yes" ]]
        then
            systemctl suspend
        else
            exit 0
        fi
        ;;
    *)
        exit 0
        ;;
    esac
fi
