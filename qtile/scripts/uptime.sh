#!/bin/sh

d=$(awk '{print int($1/86400)}' /proc/uptime)
h=$(awk '{print int($1/3600)}' /proc/uptime)
m=$(awk '{print int(($1%3600)/60)}' /proc/uptime)

if [[ $d = 0 && $h = 0 && $m < 1 ]]
then
    printf "unter 1min"
elif [[ $d = 0 && $h = 0 ]]
then
    printf $m"min"
elif [[ $d = 0 && $m = 0 ]]
then
    printf $h"h"
elif [[ $h = 0 && $m = 0 ]]
then
    printf $d"d"
elif [ $d = 0 ]
then
    printf $h"h "$m"min"
elif [ $h = 0 ]
then
    printf $d"d "$m"min"
elif [ $m = 0 ]
then
    printf $d"d "$h"h"
else
    printf $d"d "$h"h "$m"min"
fi