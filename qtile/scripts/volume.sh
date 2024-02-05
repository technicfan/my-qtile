#!/bin/bash

function diff()
{
    int=$(echo $(bc <<< "$@/5"))
    float=$(echo $(bc <<< "scale=1; $@/5"))
    diff=$(echo $(bc <<< "scale=1; $float-$int"))
}

if [ $1 = "increase" ]
then
    difference=+5
    while_change=-1
elif [ $1 = "decrease" ]
then
    difference=-5
    while_change=+1
else
    exit
fi

current_vol=$(amixer sget Master | awk -F "[][]" '/Left:/ { print $2 }' | awk -F "%" '{print $1}')

if [ -z "$current_vol" ]
then
    new_vol=$(($(amixer sget Master | awk -F "[][]" '/Mono:/ { print $2 }' | awk -F "%" '{print $1}')$difference))
else
    new_vol=$(($current_vol$difference))
fi

diff $new_vol

while [ $diff != 0 ]
do
    new_vol=$(($new_vol$while_change))
    diff $new_vol
done

amixer sset Master $new_vol%