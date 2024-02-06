#!/bin/sh

# set mouse name here:
mouse="Razer Razer Basilisk V3"

for i in 1 2 
do
    id=$(xinput --list | grep "↳ $mouse" | grep -n "pointer" | grep -no "id=.." | grep -Po "$i:id=\K..")
    xinput --set-prop $id "Coordinate Transformation Matrix" 0.45 0 0 0 0.45 0 0 0 1
done
