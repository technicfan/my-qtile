#!/bin/bash

function run {
  if ! pgrep -x $(basename $1 | head -c 15) 1>/dev/null;
  then
    $@&
  fi
}

#change your keyboard if you need it
setxkbmap -layout de

# Arcolinux-text-dark-rounded-1080p.png
# Archlinux-text-dark-rounded-1080p.png
# linux.png
# retro-arco.png

# Arcolinux
feh --bg-fill "/home/technicfan/.config/qtile/wallpapers/Arcolinux-text-dark-rounded-1080p.png" &

# Archlinux
#feh --bg-fill "path/to/wallpaper" &

#starting utility applications at boot time
run nm-applet &
run xfce4-power-manager &
#numlockx on &
blueman-applet &
picom --config /home/technicfan/.config/picom/picom.conf &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
/usr/lib/xfce4/notifyd/xfce4-notifyd &
/usr/lib/kdeconnectd &
aw-qt &
polychromatic-tray-applet &
nextcloud &
caffeine &

input-remapper-control --command autoload &
polychromatic-cli -o spectrum &
polychromatic-cli -o brightness -p 50 &
polychromatic-cli --dpi 2600 &

.config/qtile/scripts/mouse.sh &
