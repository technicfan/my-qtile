#!/bin/bash

main()
{
    for i in $(seq 1 $(ls -1 ~/VirtualBox\ VMs | wc -l))
    do
        local options[$i]=$(ls -m ~/VirtualBox\ VMs | awk -F ", " '{ print $(shell_var='"$i"') }' )
    done

    local choice=$(printf '%s\n' "-> Wine" "${options[@]}" | $DMENU $DMENU_POS 'Wine/VM:')

    if [[ -n $choice && "${options[*]}" = *"$choice"* ]]
    then
        if [[ "$(echo -e "No\nYes" | $DMENU $DMENU_POS "Start VM \"$choice\"?")" == "Yes" ]]
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

        local choice=$(printf '%s\n' "${options[@]}" | $DMENU $DMENU_POS 'Run:')

        case $choice in
        "Delphi 7")
            wine "$HOME/.wine/drive_c/Program Files (x86)/Borland/Delphi7/Bin/delphi32.exe"
            ;;
        *)
            exit 0
        esac
    fi
}

main
