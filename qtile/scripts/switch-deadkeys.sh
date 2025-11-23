#!/bin/env bash

info=$(setxkbmap -query)
layout=$(grep "layout" <<<"$info" | sed 's/.*: *//g')
if grep -q "variant:.*nodeadkeys" <<<"$info"
then
    setxkbmap -layout "$layout"
else
    setxkbmap -layout "$layout" nodeadkeys
fi
