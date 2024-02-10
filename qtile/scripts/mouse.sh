#!/bin/sh

# set mouse name here
mouse="Razer Razer Basilisk V3"
# set sensitivity here
sensi="0.45"

for i in 1 2 
do
    id=$(xinput --list | grep "↳ $mouse" | grep -n "pointer" | grep -no "id=.." | grep -Po "$i:id=\K..")
    xinput --set-prop $id "Coordinate Transformation Matrix" $sensi 0 0 0 $sensi 0 0 0 1
done
