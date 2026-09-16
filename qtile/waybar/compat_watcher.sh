#!/bin/env bash

curl -s "localhost:3001/${1}/${WAYBAR_OUTPUT_NAME}"

while true; do
    inotifywait -qq -e open ~/.config/qtile/waybar/window-change && curl -s "localhost:3001/${1}/${WAYBAR_OUTPUT_NAME}"
done
