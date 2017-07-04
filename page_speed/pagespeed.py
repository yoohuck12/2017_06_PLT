__author__ = 'jnejati'

import experiments
import convert
import post_analyze
import apache_conf
import network_emulator
from urllib.parse import urlparse
import  chromium_driver
import modifications as modify
from bs4 import BeautifulSoup
import urllib.request
import urllib.response
import io
import gzip
import subprocess


def main():
    input_file = 'mixed200.txt'
    #exp_type = 'compression'
    exp_type = 'minification'
    my_profiles = [
                  {'conn_type':'wifi-fast',
                  'device_type': 'mobile',
                  'page_type': 'mixed200',
                  'cache': 'no_cache',
                  'download_rate':'100Mbit',
                  'download_delay':'2ms',
                  'download_loss':'0.1%',
                  'upload_rate':'90Mbit',
                  'upload_delay':'2ms',
                  'upload_loss':'0.1%'},
                   #3G
                   {'conn_type':'wifi-fast-delayed',
                  'device_type': 'mobile',
                  'page_type': 'mixed200',
                  'cache': 'no_cache',
                  'download_rate':'100Mbit',
                  'download_delay':'150ms',
                  'download_loss':'0.1%',
                  'upload_rate':'90Mbit',
                  'upload_delay':'150ms',
                  'upload_loss':'0.1%'},
                   # Wi-Fi ac
                   {'conn_type':'wifi-slow',
                  'device_type': 'mobile',
                  'page_type': 'mixed200',
                  'cache': 'no_cache',
                  'download_rate':'2Mbit',
                  'download_delay':'2ms',
                  'download_loss':'0.1%',
                  'upload_rate':'786Kbit',
                  'upload_delay':'2ms',
                  'upload_loss':'0.1%'},
                   #Sattelite
                   {'conn_type':'wifi-slow-delayed',
                  'device_type': 'mobile',
                  'page_type': 'mixed200',
                  'cache': 'no_cache',
                  'download_rate':'2Mbit',
                  'download_delay':'150ms',
                  'download_loss':'0.1%',
                  'upload_rate':'768Kbit',
                  'upload_delay':'150ms',
                  'upload_loss':'0.1%'}
                                        ]

                   # Wolfinet-Guest


    for net_profile in my_profiles:
        print('Current profile: ' + net_profile['device_type'] + ' - ' + net_profile['conn_type'])
        apachectl_orig = apache_conf.ApacheConf(net_profile['device_type'], net_profile['conn_type'], input_file.split('.')[0], 'orig', '/home/jnejati')
        #apachectl_modified = apache_conf.ApacheConf('mobile', net_profile['conn_type'], input_file.split('.')[0], exp_type, '/home/jnejati')
        apachectl_orig.a2ensite('original.testbed.localhost')
        apachectl_orig.restart_apache()
        #apachectl_modified.a2ensite('modified.testbed.localhost')
        #apachectl_modified.restart_apache()
        apachectl_orig.initialize_archive_dir()
        for run_no in range(1):
            top_sites = (l.strip().split() for l in open("./res/" + input_file).read().splitlines())
            for site in top_sites:
                s1 = urlparse(site[0])
                if s1.scheme:
                    apachectl_orig.fetch_site(s1.geturl())
                else:
                    print("Use FQDN in your input site list")
                    break
                apache_conf.ApacheConf.restart_apache()
                netns = network_emulator.NetworkEmulator(net_profile)
                netns.set_profile(net_profile['conn_type'])
                my_run = chromium_driver.RunChromium(site[0], 'orig',  net_profile)
                my_run.main_run()
                conv_orig = convert.Convert()
                if conv_orig.do_analysis(net_profile, 'orig', exp_type):
                    print("Origin json file analyzed")
                    #my_exp = experiments.SetExperiment(exp_type)
                    #print('site[0]', site[0])
                    #my_exp.run(site[0], my_profiles[0])
                    #conv_mod = convert.Convert()
                    #conv_mod.do_analysis(my_profiles[0], 'modified', exp_type)
                else:
                    print("No origin json file for this site")
                apachectl_orig.archive_site(s1.netloc)
                #apachectl_modified.archive_site(s1.netloc)

        post_analyze.run(net_profile, 'orig', exp_type)
        #post_analyze.run(net_profile, 'modified', exp_type)

if __name__ == '__main__':
    main()

# Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)' ' Chrome/41.0.2228.0 Safari/537.36'
# my_request = urllib.request.Request('http://www.flickr.com', headers=headers_dict)
# my_request = urllib.request.Request('http://www.flickr.com')
# my_request.add_header('Accept-encoding', 'gzip')


# response = urllib.request.urlopen(my_request)
#print(response.info())
#print(response.getcode())
#print(urllib.request.HTTPRedirectHandler().inf_msg)



"""if response.info().get('Content-Encoding') == 'gzip':
    print('ddd')
    buf = io.BytesIO(response.read())
    f = gzip.GzipFile(fileobj=buf)
    data = f.read()

headers = (response.info())
print(headers)
html = response.read()
soup = BeautifulSoup(html)
print(soup)"""