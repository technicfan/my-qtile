#!/bin/sh

xrandr --output DP-4 --auto --output HDMI-0 --auto --right-of DP-4

cd /home/technicfan/.config/qtile/screens

touch 2 && rm 1