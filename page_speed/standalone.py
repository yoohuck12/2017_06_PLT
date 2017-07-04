__author__ = 'jnejati'
import subprocess
import sys
import os
import time

def main():

    logfile = open('./my_log.txt', 'a+')
    command = ['/home/jnejati/android-sdk-linux/tools/monkeyrunner', './testshell.py']
    try:
        proc = subprocess.call(command, shell=False, timeout=60)
        print("Cookies cleared")
    except subprocess.TimeoutExpired:
        print("Killed process " + " after timeout")

    try:
        subprocess.call(['/home/jnejati/android-sdk-linux/platform-tools/adb', 'logcat', '-c'], shell=False, timeout=20)
    except subprocess.TimeoutExpired:
        print("Killed process " + 'logcat -c' + " after timeout")

    print('Now running testshell')
    main_activity = 'org.chromium.chrome.testshell/org.chromium.chrome.testshell.ChromiumTestShellActivity'
    loadcommand = ['/home/jnejati/android-sdk-linux/platform-tools/adb', 'shell', 'am', 'start', '-n', 'org.chromium.chrome.testshell/org.chromium.chrome.testshell.ChromiumTestShellActivity', 'http://original.testbed.localhost/www.facebook.com/']
    log_command = ['/home/jnejati/android-sdk-linux/platform-tools/adb', 'logcat', "*:E"]

    try:
        proc1 = subprocess.call(log_command, stdout=logfile, shell=False, timeout=75)
        proc2 = subprocess.call(loadcommand, shell=False, timeout=60)

    except subprocess.TimeoutExpired:
        print("Killed process " + 'www.facebook.com' + " after timeout")
    logfile.close()


if __name__ == '__main__':
    main()
