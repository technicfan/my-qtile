#!/bin/bash

main()
{
    for i in $(seq 1 $(ls -1 ~/VirtualBox\ VMs | wc -l))
    do
        local options[$i]=$(ls -m ~/VirtualBox\ VMs | awk -F ", " '{ print $(shell_var='"$i"') }' )
    done

    local choice=$(printf '%s\n' "-> Wine" "${options[@]}" | $DMENU $DMENU_POS 'Wine/VM:')


    if [[ $choice = "-> Wine" ]]
    then
        local options=(
            "Remarkable Desktop"
            "Delphi 7"
        )

        local choice=$(printf '%s\n' "${options[@]}" | $DMENU $DMENU_POS 'Run:')

        case $choice in
        "Remarkable Desktop")
            wine "$HOME/.wine/drive_c/Program Files (x86)/reMarkable/reMarkable.exe"
            ;;
        "Delphi 7")
            wine "$HOME/.wine/drive_c/Program Files (x86)/Borland/Delphi7/Bin/delphi32.exe"
            ;;
        *)
            exit 0
        esac
    elif [[ -n $choice ]]
    then
        if [[ "$(echo -e "No\nYes" | $DMENU $DMENU_POS "Start VM \"$choice\"?")" == "Yes" ]]
        then
            local file=$(ls -1 "$HOME/VirtualBox VMs/$choice/" | grep .vbox | grep -n "" | grep 1: | awk -F ":" '{ print $2 }')
            local vm=$(cat "$HOME/VirtualBox VMs/$choice/$file" | grep "Machine uuid" | awk -F "=" '{ print $3}' | awk -F "\"" '{ print $2 }')
            if [[ -n $vm ]]
            then
                notify-send "starting VM \"$choice\""
                virtualboxvm --startvm "$vm"
            else
                notify-send "VM \"$choice\" not found"
            fi
        else
            exit 0
        fi
    fi
}

main
