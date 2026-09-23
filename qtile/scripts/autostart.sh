#!/bin/bash

# rounded corners
radius=$(grep "corner-radius" ~/.config/qtile/picom/picom.conf | awk -F " = " '{print $2}')
if [[ $radius != 0 ]]
then
    xcorners -b -r "$radius" &
fi

# mouse sensitivity
# ~/.config/qtile/scripts/mouse.sh "Razer Basilisk V3" &

# stupid libadwaita dark bug fix
if [[ $(gsettings get org.gnome.desktop.interface color-scheme) != "'prefer-dark'" ]]
then
    gsettings set org.gnome.desktop.interface color-scheme prefer-dark &
fi &

# fix environment for xdg-desktop-portal-wlr?
systemctl --user import-environment WAYLAND_DISPLAY

# uwsgi --plugin python ~/.config/qtile/waybar/uwsgi.ini &
waybar &

#starting utility applications at boot time
nm-applet &
xfce4-power-manager &
blueman-applet &
# picom -b --config .config/qtile/picom/picom.conf &
# xcompmgr -n &
bitwarden-desktop &
# goldwarden daemonize &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
dunst &
/usr/lib/kdeconnectd &
awatcher --no-tray &
# ( sleep 4 && aw-sync --sync-dir "$HOME/Nextcloud/technicfan/Nextcloud/Linux/activitywatch" ) &
# nextcloud &
# tutanota-desktop -a &
caffeine &
caffeine-indicator &
clipcatd -r &
flameshot &

#change your keyboard if you need it
setxkbmap -layout de nodeadkeys &
