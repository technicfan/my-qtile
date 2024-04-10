#!/bin/bash

main()
{
    for i in $(seq 1 $(ls -1 ~/VirtualBox\ VMs | wc -l))
    do
        local vms[$i]=$(ls -m ~/VirtualBox\ VMs | awk -F ", " '{ print $(shell_var='"$i"') }' )
    done

    local choice=$(printf '%s\n' "${vms[@]}" | $DMENU 'Choose VM:')

    if [[ -n $choice && "$(echo -e "No\nYes" | $DMENU "Start VM \"$choice\"?")" == "Yes" ]]
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
}

main
