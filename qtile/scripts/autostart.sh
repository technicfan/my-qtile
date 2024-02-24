#!/bin/bash

function run {
  if ! pgrep -x $(basename $1 | head -c 15) 1>/dev/null;
  then
    $@&
  fi
}

# screen config
~/.config/qtile/scripts/screens.sh restore &

# mpris widget init
~/.config/qtile/scripts/widgetboxes.sh mpris hidden &

# wallpaper
~/.config/qtile/scripts/screens.sh wallpaper &

# mouse sensitivity
~/.config/qtile/scripts/mouse.sh &

#change your keyboard if you need it
setxkbmap -layout de

#starting utility applications at boot time
run nm-applet &
run xfce4-power-manager &
blueman-applet &
picom -b --config .config/picom/picom.conf &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
/usr/lib/xfce4/notifyd/xfce4-notifyd &
clipcatd -r &
/usr/lib/kdeconnectd &
aw-qt &
#polychromatic-tray-applet &
nextcloud &
caffeine &

input-remapper-control --command autoload &
~/.config/qtile/scripts/numlock.sh match &
polychromatic-cli -e mouse &
polychromatic-cli -e mousepad &
polychromatic-cli -o brightness -p 50 &
polychromatic-cli --dpi 2600 &
