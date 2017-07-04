#!/bin/bash -x
echo "=========== START ========================"
# 1. Install the application
site=$1
logfile=$2
echo $lofgile
echo "Starting"
adb uninstall "org.chromium.chrome.testshell" # Uninstall application if already installed
adb logcat -c # Clear log buffer
adb install "../chrome/ChromiumTestShell.apk" # Install the application

# 2. Launch the application
adb logcat -c
#sleep 2 # wait for 50 sec
adb shell am start -n "org.chromium.chrome.testshell"/"org.chromium.chrome.testshell.ChromiumTestShellActivity" # Launch the application
sleep 2 # wait for 50 sec
#/home/jnejati/android-sdk-linux/platform-tools/adb shell am start -n "org.chromium.chrome.testshell"/"org.chromium.chrome.testshell.ChromiumTestShellActivity"  $site
#sleep 2 # wait for 50 sec

#adb shell su -c 'rm -rf /data/data/org.chromium.chrome.testshell/cache'
#sleep 2
adb shell am start -n "org.chromium.chrome.testshell"/"org.chromium.chrome.testshell.ChromiumTestShellActivity"  $site
#/home/jnejati/android-sdk-linux/platform-tools/adb logcat *:E | tee $logfile
adb logcat *:E> $logfile &

sleep 20 # wait for 50 sec
# get pid of adb logcat
kill -9 `ps -ef | grep "adb logcat" | awk '{print $2}'`
exit 0
echo "=========== END ========================"
