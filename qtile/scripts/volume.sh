#!/bin/bash

diff()
{
    local int=$(echo $(bc <<< "$1/5"))
    local float=$(echo $(bc <<< "scale=1; $1/5"))
    local diff=$(echo $(bc <<< "scale=1; $float-$int"))
    echo $diff
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

set()
{
    amixer sset Master $new_vol%
}

in_de()
{
    local new_vol=$(($(get)$1))

    diff=$(diff $new_vol)

    while [ $diff != 0 ]
    do
        new_vol=$(($new_vol$2))
        diff=$(diff $new_vol)
    done

    set $new_vol
}

check()
{
    local current_vol=$(get)
    
    if [[ $(diff $current_vol) != 0 ]]
    then
        local vol=0

        while (( $vol < $current_vol ))
        do
            local vol=$(($vol + 5))
        done

        if [[ $(($vol - $current_vol)) < 4 ]]
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
}

main()
{
    case $1 in
    "increase")
        in_de +5 -1
        ;;
    "decrease")
        in_de -5 +1
        ;;
    "toggle")
        amixer sset Master $1
        exit 0
        ;;
    "get")
        check
        ;;
    *)
        exit 1
    esac
}

main $1