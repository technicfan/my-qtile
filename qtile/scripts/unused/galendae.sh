#!/bin/sh

check()
{
    local exit=$(awk -F " = " '/'$1'/ {print $2}' ~/.config/qtile/states/states.ini)

    if [[ $exit = 1 || $exit = 0 ]]
    then
        return $exit
    else
        exit 1
    fi
}

if check tray
then
    galendae
else
    galendae -c ~/.config/galendae/galendae-mouse.conf
fi