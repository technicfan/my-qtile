#!/bin/sh

check()
{
    if ! cat ~/.config/qtile/states/states.conf
    then
        cp ~/.config/qtile/states/default-states.conf ~/.config/qtile/states/states.conf
    fi
    
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