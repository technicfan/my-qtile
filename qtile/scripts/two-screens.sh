#!/bin/sh

xrandr --output DP-4 --auto --output HDMI-0 --auto --right-of DP-4

cd /home/technicfan/.config/qtile/screens

touch 2 && rm 1

# Arcolinux-text-dark-rounded-1080p.png
# Archlinux-text-dark-rounded-1080p.png
# linux.png
# retro-arco.png

# Arcolinux
feh --bg-fill "/home/technicfan/.config/qtile/wallpapers/Arcolinux-text-dark-rounded-1080p.png" &

# Archlinux
#feh --bg-fill "path/to/wallpaper" &