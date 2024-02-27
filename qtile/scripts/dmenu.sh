#!/bin/bash

# technicfan
#dmenu="dmenu -i -l 20 -nb #133912 -nf #87a757 -sb #87a757 -sf #133912 -fn 'JetBrains:bold:pixelsize=14'"

# gruvbox
dmenu="dmenu -i -l 20 -nb #282828 -nf #dfbf8e -sb #dfbf8e -sf #282828 -fn 'JetBrains:bold:pixelsize=14'"
dmenu_width=" -z 300 -p"
locker="i3lock-fancy-dualmonitor"

process-manager()
{
    dmenu_width=" -z 960 -p"

    selected="PID CMD"

    while [[ $selected = "PID CMD" ]]
    do
        selected="$(ps --user "$USER" -F | $dmenu $dmenu_width "Kill process:" | awk '{print $2" "$11}')"
    done

    echo $(echo $selected | awk -F " " '{ print $1 }')

    if [[ -n $selected ]]
    then
        if [[ $(echo -e "No\nYes" | $dmenu $dmenu_width  "Kill $selected?") == "Yes" ]]
        then
            kill "$(echo $selected | awk -F " " '{ print $1 }')"
            exit 0
        else
            exit 1
        fi
    fi
}

output-switcher()
{
    local dmenu_width=" -z 400 -p"

    get_default_sink() {
        pactl --format=json info | jq -r .default_sink_name
    }

    get_all_sinks() {
        pactl --format=json list short sinks \
            | current=$(get_default_sink) jq -r '.[] | if .name == env.current then .state="* " else .state="" end | .state + .name'
    }

    local choice=$(printf '%s\n' "$(get_all_sinks)" | sort | $dmenu $dmenu_width 'Sink:') || exit 1

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

logout()
{
    local options=(
        "Lock"
        "Logout"
        "Reboot"
        "Shutdown"
        "Suspend"
    )

    local choice=$(printf '%s\n' "${options[@]}" | $dmenu $dmenu_width 'Power menu:')

    case $choice in
    "Lock")
        ${locker}
        ;;
    "Logout")
        if [[ "$(echo -e "No\nYes" | $dmenu $dmenu_width "${choice}?")" == "Yes" ]]
        then
            pkill -KILL -u $USER
        else
            exit 1
        fi
        ;;
    "Reboot")
        if [[ "$(echo -e "No\nYes" | $dmenu $dmenu_width "${choice}?")" == "Yes" ]]
        then
            systemctl reboot
        else
            exit 0
        fi
        ;;
    "Shutdown")
        if [[ "$(echo -e "No\nYes" | $dmenu $dmenu_width "${choice}?")" == "Yes" ]]
        then
            systemctl poweroff
        else
            exit 0
        fi
        ;;
    "Suspend")
        if [[ "$(echo -e "No\nYes" | $dmenu $dmenu_width "${choice}?")" == "Yes" ]]
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

# stolen from Luke Smith
unicode()
{
    local dmenu_width="-z 400 -p"

    # Get user selection via dmenu from emoji file.
    local chosen=$(cut -d ';' -f1 ~/.config/qtile/chars/* | $dmenu $dmenu_width 'Emoji Picker:' | sed "s/ .*//")

    # Exit if none chosen.
    [ -z "$chosen" ] && exit

    #show a message that the emoji has been copied.
    printf "%s" "$chosen" | xclip -selection clipboard
	notify-send "'$chosen' copied to clipboard." &
}

monitor()
{
    local options=(
        "Monitor 1"
        "Monitor 2"
        "Both Monitors"
        "Mirror"
        "Off"
    )

    local choice=$(printf '%s\n' "${options[@]}" | $dmenu $dmenu_width 'Monitors:')

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

wine_vm()
{
    for i in $(seq 1 $(ls -1 ~/VirtualBox\ VMs | wc -l))
    do
        local options[$i]=$(ls -m ~/VirtualBox\ VMs | awk -F ", " '{ print $(shell_var='"$i"') }' )
    done

    local choice=$(printf '%s\n' "-> Wine" "${options[@]}" | $dmenu $dmenu_width 'Wine/VM:')

    if [[ -n $choice && "${options[*]}" = *"$choice"* ]]
    then
        if [[ "$(echo -e "No\nYes" | $dmenu $dmenu_width "Start VM \"$choice\"?")" == "Yes" ]]
        then
            local file=$(ls -1 "$HOME/VirtualBox VMs/$choice/" | grep .vbox | grep -n "" | grep 1: | awk -F ":" '{ print $2 }')
            local vm=$(cat "$HOME/VirtualBox VMs/$choice/$file" | grep "Machine uuid" | awk -F "=" '{ print $3}' | awk -F "\"" '{ print $2 }')
            if [[ -n $vm ]]
            then
                virtualboxvm --startvm "$vm"
            else
                notify-send "VM \"$choice\" not found"
            fi
        else
            exit 0
        fi
    elif [[ $choice = "-> Wine" ]]
    then
        local options=(
            "Delphi 7"
        )

        local choice=$(printf '%s\n' "${options[@]}" | $dmenu $dmenu_width 'Run:')

        case $choice in
        "Delphi 7")
            wine "$HOME/.wine/drive_c/Program Files (x86)/Borland/Delphi7/Bin/delphi32.exe"
            ;;
        *)
            exit 0
        esac
    fi
}

case $1 in
"kill")
    process-manager
    ;;
"output-switcher")
    $1
    ;;
"logout")
    $1
    ;;
# stolen from Luke Smith
"unicode")
    $1
    ;;
# own
"monitor")
    $1
    ;;
"wine_vm")
    $1
    ;;
"dmenu")
    if [[ -n $2 ]]
    then
        $dmenu$dmenu_width "$2"
    else
        exit 1
    fi
    ;;
*)
    exit 1
esac
