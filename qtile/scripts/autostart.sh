#!/bin/bash

# wallpaper
~/.config/qtile/scripts/screens.sh wallpaper &

# rounded corners
#xcorners -b -r $(cat ~/.config/qtile/picom/picom.conf | grep corner-radius | awk -F " = " '{print $2}') &

# mouse sensitivity
~/.config/qtile/scripts/mouse.sh "Razer Basilisk V3" &

# mpris widgetbox
~/.config/qtile/scripts/widgetbox.py reset

#change your keyboard if you need it
setxkbmap -layout de

#starting utility applications at boot time
nm-applet &
xfce4-power-manager &
blueman-applet &
picom --config .config/qtile/picom/picom.conf &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
dunst &
/usr/lib/kdeconnectd &
aw-qt --no-gui &
nextcloud &
#caffeine &
clipcatd -r &
unclutter -idle 3 &
flameshot &

nvidia-settings --assign FXAA=1 &
nvidia-settings -l &
input-remapper-control --command autoload &
polychromatic-cli -e keyboard &
polychromatic-cli -e mouse &
polychromatic-cli -e mousepad &
polychromatic-cli -o brightness -p 50 &
polychromatic-cli --dpi 2300 &
