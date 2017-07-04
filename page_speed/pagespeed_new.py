__author__ = 'jnejati'

import experiments
import convert
import post_analyze
import apache_conf
import network_emulator
from urllib.parse import urlparse
import  chromium_driver
import os
import shutil
import modifications as modify
from bs4 import BeautifulSoup
import urllib.request
import urllib.response
import io
import gzip
import subprocess
import time

"""Bandwidth 1  5 20

delay 5ms, 50ms, , 150ms

but just hold loss rate at 2%"""

def main():
    input_file = 'mixed200.txt'
    arch_dir = '/home/jnejati/page_speed/arch_dir'
    #exp_type = 'compression'
    exp_type = 'minification'
    my_profiles = [

                  {'conn_type':'wifi-n-b20-d50',
                  'device_type': 'mobile',
                  'page_type': 'mixed200',
                  'cache': 'no_cache',
                  'download_rate':'20Mbit',
                  'download_delay':'25ms',
                  'download_loss':'1%',
                  'upload_rate':'1Mbit',
                  'upload_delay':'25ms',
                  'upload_loss':'1%'},
                  ]
    apache_conf.rm_dir(arch_dir)
    apache_conf.fetch_all_sites(input_file, arch_dir)

    for run_no in range(1):
        top_sites = (l.strip().split() for l in open("./res/" + input_file).read().splitlines())
        for net_profile in my_profiles:
            for site in top_sites:
                print('Current profile: ' + net_profile['device_type'] + ' - ' + net_profile['conn_type'])
                s1 = urlparse(site[0])
                apache_conf.rm_dir('/var/www/original.testbed.localhost')
                command = ["cp", "-R", arch_dir + '/' + s1.netloc + '/.', '/var/www/original.testbed.localhost']
                try:
                    proc = subprocess.call(command, shell=False, timeout=30)
                    print(s1.netloc + ' copied')
                except subprocess.TimeoutExpired:
                    print("Couldn't copy ", s1.netloc)

                apachectl_orig = apache_conf.ApacheConf(net_profile['device_type'], net_profile['conn_type'], input_file.split('.')[0], 'orig', '/home/jnejati')
                apachectl_orig.a2ensite('original.testbed.localhost')
                apache_conf.ApacheConf.restart_apache()
                netns = network_emulator.NetworkEmulator(net_profile)
                netns.set_profile(net_profile['conn_type'])
                my_run = chromium_driver.RunChromium(site[0], 'orig',  net_profile)
                my_run.main_run()
                conv_orig = convert.Convert()
                if conv_orig.do_analysis(net_profile, 'orig', exp_type):
                    print("Origin json file analyzed")
                else:
                    print("No origin json file for this site")
                    continue
                #apachectl_orig.archive_site(s1.netloc)
                time.sleep(60)

        #for net_profile in my_profiles:
        #    post_analyze.run(net_profile, 'orig', exp_type)
        #post_analyze.run(net_profile, 'modified', exp_type)

if __name__ == '__main__':
    main()
