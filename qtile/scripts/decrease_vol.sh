#!/bin/bash

current_vol=$(amixer sget Master | awk -F "[][]" '/Left:/ { print $2 }' | awk -F "%" '{print $1}')
new_vol=$(echo "$(($current_vol-5))")

int=$(echo $(bc <<< "$new_vol/5"))
float=$(echo $(bc <<< "scale=1; $new_vol/5"))
diff=$(echo $(bc <<< "scale=1; $float-$int"))

while [ $diff != 0 ];
do
    new_vol=$(echo $(bc <<< "$new_vol+1"))

    int=$(echo $(bc <<< "$new_vol/5"))
    float=$(echo $(bc <<< "scale=1; $new_vol/5"))
    diff=$(echo $(bc <<< "scale=1; $float-$int"))
done

amixer sset Master $new_vol%