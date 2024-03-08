#!/bin/bash

function run {
  if ! pgrep -x $(basename $1 | head -c 15) 1>/dev/null;
  then
    $@&
  fi
}

# wallpaper
~/.config/qtile/scripts/screens.sh wallpaper &

# rounded corners
xcorners -b -r 10 &

# mouse sensitivity
~/.config/qtile/scripts/mouse.sh "Razer Basilisk V3" &

# numblock rgb
#~/.config/qtile/scripts/numlock.sh match &

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
aw-qt --no-gui &
nextcloud &
caffeine &

input-remapper-control --command autoload &
polychromatic-cli -e keyboard+numblock &
polychromatic-cli -e mouse &
polychromatic-cli -e mousepad &
polychromatic-cli -o brightness -p 50 &
polychromatic-cli --dpi 2300 &
