#!/bin/bash

main()
{
    local DMENU_WIDTH="-z 400 -p"

    local chosen=$(cut -d ';' -f1 ~/.config/qtile/chars/* | $DMENU $DMENU_WIDTH 'Emoji Picker:' | sed "s/ .*//")

    [ -z "$chosen" ] && exit

    printf "%s" "$chosen" | xclip -selection clipboard
	notify-send "'$chosen' copied to clipboard." &
}

main
