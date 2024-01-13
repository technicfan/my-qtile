#!/bin/sh

d=$(awk '{print int($1/86400)}' /proc/uptime)
h=$(awk '{print int($1/3600)}' /proc/uptime)
m=$(awk '{print int(($1%3600)/60)}' /proc/uptime)

if [[ $d -eq 0 && $h -eq 0 && $m < 1 ]]; then
    printf "unter 1min"
elif [[ $d -eq 0 && $h -eq 0 ]]; then
    printf $m"min"
elif [[ $d -eq 0 && $m -eq 0 ]]; then
    printf $h"h"
elif [[ $h -eq 0 && $m -eq 0 ]]; then
    printf $d"d"
elif [[ $d -eq 0 ]]; then
    printf $h"h "$m"min"
elif [[ $h -eq 0 ]]; then
    printf $d"d "$m"min"
elif [[ $m -eq 0 ]]; then
    printf $d"d "$h"h"
else
    printf $d"d "$h"h "$m"min"
fi