#!/bin/sh

if [[ -n $1 ]]
then
    for i in {1..2}
    do
        id=$(xinput --list | grep "$1" | grep -v input-remapper | grep -n pointer | grep -no "id=.." | grep -Po "$i:id=\K..")
        xinput --set-prop $id "libinput Accel Profile Enabled" 0 1 0
    done
else
    exit 1
fi
