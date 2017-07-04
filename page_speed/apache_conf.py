__author__ = 'jnejati'

import fileinput
import shutil
import os
import subprocess
from urllib.parse import urlparse


def rm_dir(folder):
    if os.path.isdir(folder):
            for root, dirs, l_files in os.walk(folder):
                for f in l_files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
    else:
        os.makedirs(folder)

def fetch_site(site_name, save_dir):
    document_root = '/var/www/original.testbed.localhost'
    """headers_dict = {'User-Agent': 'Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/'
                                  '<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Mobile Safari/<WebKit Rev>'
                                  , 'Accept-encoding':'gzip'}"""

    headers_dict = {'User-Agent': 'Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/'
                                  '<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Mobile Safari/<WebKit Rev>'
        , 'Accept-encoding': 'gzip'}
    try:
        command = 'wget' + ' ' + '-nv' + ' ' + '-E' + ' ' + '-H' + ' ' + '-k' + ' ' + '-K' + ' ' + '-p' + ' ' + '-e robots=off' + ' ' + '-P' + ' ' + save_dir + ' ' + '--convert-links' + ' ' + site_name
        print("Downloading " + site_name)
        proc = subprocess.call(command.split(), shell=False, timeout=35)
        print('Fetch done')

        # print (proc.returncode)
    except subprocess.TimeoutExpired or FileExistsError:
        print("Killed process " + site_name + " after timeout")


def fetch_all_sites(input_file, arch_dir):
    top_sites = (l.strip().split() for l in open("./res/" + input_file).read().splitlines())
    if os.path.isdir(arch_dir):
        for root, dirs, l_files in os.walk(arch_dir):
            for f in l_files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
    else:
        os.makedirs(arch_dir)
    for site in top_sites:
        s1 = urlparse(site[0])
        if s1.scheme:
            if os.path.isdir(os.path.join(arch_dir, s1.netloc)):
                print(os.path.join(arch_dir, s1.netloc + ' already downloaded'))
                continue
            else:
                os.makedirs(os.path.join(arch_dir, s1.netloc))
                fetch_site(s1.geturl(), os.path.join(arch_dir, s1.netloc))
        else:
            print("Use FQDN in your input site list")
            break


class ApacheConf():
    def __init__(self, device_type, conn_type, page_type, improvement_type, base_dir):
        self.device_type = device_type
        self.conn_type = conn_type
        self.page_type = page_type
        self.improvement_type = improvement_type
        self.base_dir = base_dir


    def vhost_conf_replace(self, site_name):
        vhost_conf_file_default = './conf/default_virtual_host.txt'
        vhost_conf_file_target = '/etc/apache2/sites-available/original.testbed.localhost'
        if os.path.isfile(vhost_conf_file_target):
            os.remove(vhost_conf_file_target)
        shutil.copyfile(vhost_conf_file_default, vhost_conf_file_target)
        for line in fileinput.input(vhost_conf_file_target, inplace=True):
            print(line.replace('DocumentRoot /var/www/',
                               'DocumentRoot /var/www/original.testbed.localhost/' + site_name).rstrip())
        for line in fileinput.input(vhost_conf_file_target, inplace=True):
            print(line.replace('<Directory /var/www/>',
                               '<Directory /var/www/original.testbed.localhost/' + site_name + '/>').rstrip())

    def a2ensite(self, site_name):
        command = 'a2ensite' + ' ' + site_name
        try:
            proc = subprocess.call(command.split(), shell=False, timeout=15)
        except subprocess.TimeoutExpired:
            print("Couln't enable site" + site_name)

    def a2dissite(self, site_name):
        command = 'a2dissite' + ' ' + site_name
        try:
            proc = subprocess.call(command.split(), shell=False, timeout=15)
            print('Site disabled')
        except subprocess.TimeoutExpired:
            print("Couln't disable site" + site_name)

    @staticmethod
    def restart_apache():
        command = 'service' + ' ' + 'apache2' + ' ' + 'restart'
        try:
            proc = subprocess.call(command.split(), shell=False, timeout=20)
        except subprocess.TimeoutExpired:
            print("Restaring unsuccesful")

    def initialize_archive_dir(self):
        log_dir = '/var/log/testbed/'
        if os.path.isdir(log_dir + self.device_type + '_' + self.conn_type + '_' + self.page_type + '_' + self.improvement_type):
            for root, dirs, files in os.walk(log_dir):
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
            print('Logs directory cleared!\n')
        else:
            os.makedirs(
                log_dir + self.device_type + '_' + self.conn_type + '_' + self.page_type + '_' + self.improvement_type)

    def initialize_prelog_dir(self):
        result_path = self.base_dir + '/tests/analysis_t/pre_log'
        for root, dirs, files in os.walk(result_path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        print('Logs directory cleared!\n')

    def archive_site(self, site_name):

        archive_destination = '/var/log/testbed/' + self.device_type + '_' + self.conn_type + '_' + self.page_type + '_' + self.improvement_type
        if self.improvement_type == 'orig':
            root_dir = '/var/www/original.testbed.localhost/'
        else:
            root_dir = '/var/www/modified.testbed.localhost/'
        archive_name = os.path.join(archive_destination, site_name)
        shutil.make_archive(archive_name, 'gztar', root_dir)
        for root, dirs, files in os.walk(root_dir):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))




