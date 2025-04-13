#!/bin/bash

# rounded corners
radius=$(grep "corner-radius" ~/.config/qtile/picom/picom.conf | awk -F " = " '{print $2}')
if [[ $radius != 0 ]]
then
    xcorners -b -r "$radius" &
fi

# mouse sensitivity
~/.config/qtile/scripts/mouse.sh "Razer Basilisk V3" &

# mpris widgetbox
~/.config/qtile/scripts/widgetbox.py reset &

#change your keyboard if you need it
setxkbmap -layout de &

# stupid libadwaita dark bug fix
if [[ $(gsettings get org.gnome.desktop.interface color-scheme) != "'prefer-dark'" ]]
then
    gsettings set org.gnome.desktop.interface color-scheme prefer-dark &
fi &

#starting utility applications at boot time
nm-applet &
xfce4-power-manager &
blueman-applet &
picom -b --config .config/qtile/picom/picom.conf &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
dunst &
/usr/lib/kdeconnectd &
aw-qt --no-gui &
( sleep 4 && aw-sync --sync-dir "$HOME/Nextcloud/technicfan/Nextcloud/Linux/activitywatch" ) &
nextcloud &
tutanota-desktop -a &
caffeine &
caffeine-indicator &
clipcatd -r &
unclutter -idle 3 &
flameshot &

#spotifyd &
#nvidia-settings --assign FXAA=1 &
#nvidia-settings -l &
# keyd-application-mapper -d &
# input-remapper-control --command autoload &
polychromatic-cli -e keyboard &
polychromatic-cli -e mouse &
polychromatic-cli -e mousepad &
polychromatic-cli -o brightness -p 50 &
polychromatic-cli --dpi 2300 &
