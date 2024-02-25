#!/bin/sh

if [ \( -n "$1" -a -n "$2" \) ]
then
    for i in {1..2}
    do
        id=$(xinput --list | grep "$1" | grep -v input-remapper | grep -n pointer | grep -no "id=.." | grep -Po "$i:id=\K..")
        xinput --set-prop $id "Coordinate Transformation Matrix" $2 0 0 0 $2 0 0 0 1
    done
else
    exit 1
fi
