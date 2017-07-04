__author__ = 'jnejati'
import subprocess
import sys
import os
import time

def main():

    home_dir = '/home/jnejati'
    base_dir = '/home/jnejati/page_speed'
    chromium_path = home_dir + '/chrome/chrome'
    chromium_args = '--no-sandbox' + ' ' + '--user-data-dir'
    prelog_dir = base_dir + '/tests/analysis_t/pre_log'
    orig_site = 'http://original.testbed.localhost'
    logfile = open('./loggggg.txt', 'a+')
    subprocess.call(['killall', 'chrome'], shell=False)
    netns_com = 'ip' + ' ' + 'netns' + ' ' + 'exec' + ' ' + 'client_tb' + ' '

    try:
        command = netns_com + 'sudo' + ' ' + '-u' + ' ' + 'jnejati' + ' ' + chromium_path + ' ' + chromium_args + ' ' + orig_site + '/' + 'www.huffingtonpost.com.txt'
        print("Wprof launched: " + 'www.huffingtonpost.com' + ' command: ' + command)
        proc = subprocess.call(command.split(), env={"DISPLAY": "localhost:7"}, stderr=logfile, shell=False,
                               timeout=50)
        # print (proc.returncode)
    except subprocess.TimeoutExpired:
        print("Killed process " + " after timeout")

    logfile.close()
if __name__ == '__main__':
    main()
