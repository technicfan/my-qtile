#!/bin/env bash

! [ -f ~/.config/qtile/waybar/status-change ] && touch ~/.config/qtile/waybar/status-change
curl -s "localhost:3001/${1}/${WAYBAR_OUTPUT_NAME}"

while true; do
    inotifywait -qq -e open ~/.config/qtile/waybar/status-change && curl -s "localhost:3001/${1}/${WAYBAR_OUTPUT_NAME}"
done
