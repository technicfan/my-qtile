#!/bin/bash

main()
{
    local apps=(
        "Remarkable Desktop"
        "Delphi 7"
        "BiBox"
        "ChatGPT"
        "Proton Mail"
        "Wolfenstein 3D"
        "xampp-manager"
        "Minecraft Bedrock Launcher"
    )

    local commands=(
        "$HOME/.wine/drive_c/Program Files (x86)/reMarkable/reMarkable.exe"
        "$HOME/.wine/drive_c/Program Files (x86)/Borland/Delphi7/Bin/delphi32.exe"
        "chromium --app=https://bibox2.westermann.de/shelf"
        "chromium --app=https://chat.openai.com/"
        "chromium --app=https://mail.proton.me"
        "dosbox '/mnt/Games/Heroic/Wolfenstein 3D/Wolf3d.exe'"
        "gksu manager-linux-x64.run"
        "$HOME/Applications/Minecraft*.AppImage"
    )

    local choice=$(printf '%s\n' "-> VMs" "$(printf '%s\n' "${apps[@]}" | sort)" | $DMENU 'Aliases:')


    if [[ $choice = "-> VMs" ]]
    then

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

    elif [[ -n $choice ]]
    then

        for i in $(seq 0 $((${#apps[@]} - 1)))
        do
            if [[ ${apps[i]} = $choice ]]
            then
                if [[ $i = 0 || $i = 1 ]]
                then
                    wine "${commands[i]}"
                    exit 0
                else
                    ${commands[i]}
                    exit 0
                fi
            fi
        done

    fi
}

main
