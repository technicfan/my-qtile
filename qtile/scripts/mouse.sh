#!/bin/sh

if [ -n "$1" ]
then
    for i in \
        $(xinput --list | grep -E "$1|keyd" | grep -v input-remapper |\
          grep pointer | awk -F "=" '{print $2}' | awk '{print $1}')
    do
        xinput --set-prop "$i" "libinput Accel Profile Enabled" 0 1 0
    done
else
    exit 1
fi
