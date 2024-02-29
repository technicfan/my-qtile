#!/bin/sh

check()
{
    local exit=$(cat ~/.config/qtile/states/states.conf | awk -F " = " '/'$1'/ {print $2}')

    if [[ $exit = 1 || $exit = 0 ]]
    then
        return $exit
    else
        exit 1
    fi
}

if check systray
then
    galendae
else
    galendae -c ~/.config/galendae/galendae-mouse.conf
fi