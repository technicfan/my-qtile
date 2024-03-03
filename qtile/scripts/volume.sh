#!/bin/bash

diff()
{
    echo $(($1 % $2))
}

get()
{
    local current_vol=$(amixer sget Master | awk -F "[][]" '/Left:/ { print $2 }' | awk -F "%" '{print $1}')

    if [ -z $current_vol ]
    then
        local current_vol=$(amixer sget Master | awk -F "[][]" '/Mono:/ { print $2 }' | awk -F "%" '{print $1}')
    fi

    echo $current_vol
}

check_mute()
{
    local status=$(amixer sget Master | awk -F " " '/Left:/ { print $NF }')

    if [ -z $status ]
    then
        local status=$(amixer sget Master | awk -F " " '/Mono:/ { print $NF }')
    fi

    echo $status
}

toggle()
{
    amixer -q sset Master toggle
}

set()
{
    amixer -q sset Master $1%
}

up_down()
{
    local diff=$(diff $(get) $2)

    case $1 in
    "-")
        if ! [[ $diff = 0 ]]
        then
            local change=$((-$2 + $diff))
        else
            local change=0
        fi
        ;;
    "+")
        local change=$((-$diff))
        ;;
    *)
        exit 1
    esac

    if [[ $(check_mute) = "[off]" ]]
    then
        toggle
    fi

    set $(($(get)$1$2$1$change))
}

check()
{
    if [[ $(check_mute) = "[off]" ]]
    then
        echo "[off]"
    else
        local current_vol=$(get)
        local diff=$(diff $current_vol $1)
    
        if ! [[ $diff = 0 ]]
        then
            if [[ $diff < $(($1/2+1)) ]]
            then
                local new_vol=$(($current_vol-$diff))
            else
                local new_vol=$(($current_vol+$1-$diff))
            fi

            set $new_vol

            echo $new_vol%
        else
            echo $current_vol%
        fi
    fi
}

main()
{
    case $1 in
    "up")
        up_down + $2
        ;;
    "down")
        up_down - $2
        ;;
    "toggle")
        toggle
        ;;
    "get")
        check $2
        ;;
    "help"|"-h"|"-help"|"--help")
        echo "change volume script by technicfan"
        echo "up <number>: increase volume by number or by that number which achieves a volume divisible by number"
        echo "down <number>: decrease volume by number or by that number which achieves a volume divisible by number"
        echo "check <number>: output volume or change it next volume divisible by number and output this volume"
        echo "toggle: mute/unmute"
        ;;
    *)
        exit 1
    esac
}

main $1 $2