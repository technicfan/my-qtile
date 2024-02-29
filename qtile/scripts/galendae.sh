#!/bin/sh

if cat ~/.config/qtile/systray/0
then
    galendae
elif cat ~/.config/qtile/systray/1
then
    galendae -c ~/.config/galendae/galendae-mouse.conf
fi