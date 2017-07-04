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
    apache_conf.rm_dir(arch_dir)
    apache_conf.fetch_all_sites(input_file, arch_dir)


if __name__ == '__main__':
    main()
