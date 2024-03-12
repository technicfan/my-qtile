#!/bin/bash

main()
{
    local chosen=$(cut -d ';' -f1 ~/.config/qtile/chars/* | $DMENU $DMENU_POS 'Emoji Picker:' | sed "s/ .*//")

    [ -z "$chosen" ] && exit

    printf "%s" "$chosen" | xclip -selection clipboard
	notify-send "'$chosen' copied to clipboard." &
}

main
