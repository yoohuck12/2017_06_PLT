#!/bin/bash -x

/home/jnejati/android-sdk-linux/platform-tools/adb  kill-server
sleep 2

/home/jnejati/android-sdk-linux/platform-tools/adb start-server
echo "Starting adb"
sleep 2

#enable usb android
/home/jnejati/android-sdk-linux/platform-tools/adb  shell su -c 'setprop sys.usb.config rndis,adb'
echo 'Enabliing usb on android'
sleep 2

/home/jnejati/android-sdk-linux/platform-tools/adb -d wait-for-device

/home/jnejati/android-sdk-linux/platform-tools/adb  shell am force-stop  com.android.settings/com.android.settings.TetherSettings
echo 'Disabling usb tethering'
sleep 2

/home/jnejati/android-sdk-linux/platform-tools/adb  shell am start -n com.android.settings/com.android.settings.TetherSettings
echo "Enabling usb tehtering"
sleep 2

ifconfig usb0 up

/home/jnejati/android-sdk-linux/platform-tools/adb  shell su -c 'ifconfig usb0 192.168.42.100 netmask 255.255.255.0'
/home/jnejati/android-sdk-linux/platform-tools/adb  shell su -c 'route add  -net 130.245.145.0 netmask 255.255.255.0 gw 192.168.42.1'

# ubuntu
ifconfig usb0 192.168.42.1 netmask 255.255.255.0
#route add -net 192.168.42.0 netmask 255.255.255.0 gw 192.168.42.1


exit 0
