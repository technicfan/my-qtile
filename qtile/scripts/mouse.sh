#!/bin/sh

for i in 1 2 
do
    id=$(xinput --list | grep "↳ Razer Razer Basilisk V3" | grep -n "pointer" | grep -no "id=.." | grep -Po "$i:id=\K..")
    xinput --set-prop "$id" "Coordinate Transformation Matrix" 0.4 0 0 0 0.4 0 0 0 1
done
