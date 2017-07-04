
import time

import sys
import subprocess
import  time

sys.path.append('/home/jnejati/android-sdk-linux/tools/lib')
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice


APK = "/home/jnejati/chrome/ChromiumTestShell.apk"
PACKAGE = "org.chromium.chrome.testshell"
ACTIVITY = "org.chromium.chrome.testshell.ChromiumTestShellActivity"

device = MonkeyRunner.waitForConnection()
device.removePackage(PACKAGE) # Uninstall package if already installed
device.installPackage(APK) # Install the application
device.shell('logcat -c')

run_component = PACKAGE + '/' + ACTIVITY
device.startActivity(component=run_component) # Launch the application
time.sleep(10) # Wait 10 seconds
device.shell('logcat -c')

device.shell('am start -n org.chromium.chrome.testshell/org.chromium.chrome.testshell.ChromiumTestShellActivity http://original.testbed.localhost/www.facebook.com/')
time.sleep(50) # Wait 10 seconds
device.shell('logcat *:E > mylog.txt')
time.sleep(15)
device.removePackage(PACKAGE) # Uninstall the application
