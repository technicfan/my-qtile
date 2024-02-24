#!/bin/bash

diff()
{
    echo $(bc <<< "scale=1; $1/5" | awk -F "." '{ print $2 }')
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
    if (( $1 < 0 ))
    then
        local while_change=+1
    else
        local while_change=-1
    fi

    local new_vol=$(($(get)$1))

    diff=$(diff $new_vol)

    while [ $diff != 0 ]
    do
        new_vol=$(($new_vol$while_change))
        diff=$(diff $new_vol)
    done

    if [[ $(check_mute) = "[off]" ]]
    then
        toggle
    fi

    set $new_vol
}

check()
{
    if [[ $(check_mute) = "[off]" ]]
    then
        echo "[off]"
    else
        local current_vol=$(get)
    
        if [[ $(diff $current_vol) != 0 ]]
        then
            local vol=0

            while (( $vol < $current_vol ))
            do
                local vol=$(($vol + 5))
            done

            echo $vol - $current_vol

            if [[ $(($vol - $current_vol)) < 2 ]]
            then
                local new_vol=$vol
            else
                local new_vol=$(($vol - 5))
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
        up_down +5
        ;;
    "down")
        up_down -5
        ;;
    "toggle")
        toggle
        ;;
    "get")
        check
        ;;
    *)
        exit 1
    esac
}

main $1