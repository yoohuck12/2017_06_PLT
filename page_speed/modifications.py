__author__ = 'jnejati'

import subprocess
import os
import json
import re
import codecs
from urllib.parse import urlparse, unquote
import urllib.request
import urllib.response
from bs4 import BeautifulSoup
import codecs
from premailer import transform
import shlex
import sys

class Compression:
    @staticmethod
    def enable():
        command = 'a2enmod' + ' ' + 'deflate'
        try:
            proc = subprocess.call(command.split(), shell=False, timeout=15)
        except subprocess.TimeoutExpired:
            print("Couldn't enable deflate")

    @staticmethod
    def disable():
        command = 'a2dismod' + ' ' + 'deflate'
        try:
            proc = subprocess.call(command.split(), shell=False, timeout=15)
        except subprocess.TimeoutExpired:
            print("Couldn't disable deflate")


class Minification:
    def __init__(self, src, site_name):
        self.src = src
        self.site_name = site_name


    def already_minified(self, my_file2):
        f = codecs.open(my_file2, 'r', encoding='utf-8')
        try:
            my_chunk = f.read(50)
        except UnicodeDecodeError:
            return True
        # f = open(my_file2, 'r')
        if re.search(r"\s", my_chunk):
            return False
        else:
            return True

    def minify(self, output):
        my_file = open(output, 'a')
        reduction_dict = {str(self.site_name): []}
        print('inside minify', self.src, self.site_name)
        for root, dirs, files in os.walk(self.src):
            print(root, dirs, files)
            for file in files:
                file = file.encode('ascii', 'ignore').decode('ascii')
                print('file: ', file)
                if file.endswith('.css') or file.endswith('.js'):
                    print("Scripts found!")
                    file_path = os.path.join(root, file)
                    if not self.already_minified(file_path):
                        command = 'java' + ' ' + '-jar' + ' ' + '/home/jnejati/page_speed/libs/yuicompressor-2.4.8.jar' + ' ' + file_path + ' ' + '-o' + ' ' + file_path
                        reduction_dict[str(self.site_name)].append(file)
                        reduction_dict[str(self.site_name)].append(os.stat(file_path).st_size)  # in bytes
                        try:
                            print('trying to run java')
                            proc = subprocess.call(command.split(), shell=False, timeout=20)
                            reduction_dict[str(self.site_name)].append(os.stat(file_path).st_size)
                        except subprocess.TimeoutExpired:
                            print("Couldn't minify" + file)
                    else:
                        print(file + ' already minified')
                else:
                    print('inside minify, no script found')
        json.dump(reduction_dict, my_file)
        print('dict', reduction_dict)


class Inline:
    def __init__(self, base_dir,site_name):
        self.site_name = site_name
        self.base_dir = base_dir  # /var/www/modified.testbed.localhost'
        self.s1 = urlparse(self.site_name)
        output_dir = '/home/jnejati/page_speed/inline_output'
    def get_content(self, script_path):
        try:
            my_file = codecs.open(os.path.normpath(os.path.join(self.base_dir, self.s1.netloc, script_path)), 'r',
                                  "utf-8")
        except FileNotFoundError:
            print(os.path.normpath(os.path.join(self.base_dir, self.s1.netloc, script_path)) + ' not found')
        file_stat = os.stat(os.path.normpath(os.path.join(self.base_dir, self.s1.netloc, script_path)))
        script_size = file_stat.st_size
        script_content = my_file.read()
        return script_content, script_size
    
    def rename(self, exp_type):
        command = ["mv", self.base_dir+'/' + self.s1.netloc+'/index.html', self.base_dir+'/' + self.s1.netloc+'/index.html_before'+exp_type]
        try:
            proc = subprocess.call(command, shell=False, timeout=30)
            print('original index.html renamed')
        except subprocess.TimeoutExpired:
            print("couldn't rename original index.html")

    def replace_javascript(self, soup):

        # TODO size, ...
        files = {}
        for js in soup.find_all('script', src=True):
            try:
                real_js, file_size = self.get_content(unquote(js['src']))
                if file_size != 0:
                    new_tag = soup.new_tag("script")
                    new_tag.string = real_js
                    js.replace_with(new_tag)
                    print('In js inliner', js['src'], file_size)
                    files[js['src']]=file_size

            except FileNotFoundError or TypeError:
                print('In js inliner: File not found')
        
        html = soup.prettify(soup.original_encoding)
        self.rename('jsinlining')
        with open((self.base_dir +'/'+self.s1.netloc + '/index.html'), 'wb') as f:
            f.write(html)
        return soup,files

    def replace_css(self, soup):
        files = {}
        for link in soup.find_all('link', rel="stylesheet"):
            try:
                real_css, file_size = self.get_content(unquote(link["href"]))
                if file_size != 0:
                    new_tag = soup.new_tag("style")
                    new_tag.string = real_css
                    link.replace_with(new_tag)
                    print('In css inliner', unquote(link["href"]),  file_size)
                    files[link['href']]=file_size
            except FileNotFoundError or TypeError:
                print('In js inliner: File not found')

        html = soup.prettify(soup.original_encoding)
        #print('Type: ', type(html))
        self.rename('cssinlining')
        with open((self.base_dir +'/' + self.s1.netloc + '/index.html'), 'wb') as f:
            f.write(html)
        return soup,files
 
    def inliner(self):
        print(self.base_dir,self.s1.netloc)
        try:
             response = urllib.request.urlopen('file://' + os.path.join(self.base_dir, self.s1.netloc, 'index.html'))
             print('index:', os.path.join(self.base_dir, self.s1.netloc, 'index.html'))
             html = response.read()
             bs = BeautifulSoup(html, 'html5lib')
             js_bs,js_files = self.replace_javascript(bs)
             f = open('/home/jnejati/page_speed/inline_output/' + self.s1.netloc, 'w+')
             for key, value in js_files.items():
                 f.write(key + '\t' + str(value) + '\n')
             """css_bs,css_files = self.replace_css(js_bs)
             for key, value in css_files.items():
                 f.write(key + '\t' + str(value) + '\n')"""
             #print('Details of Inlined files: '+ self.base_dir+'/'+ self.s1.netloc +'/'+self.s1.netloc + '/inlined_files.txt')
        except FileNotFoundError:
             f = open('/home/jnejati/page_speed/inline_output/' + self.s1.netloc, 'w+')
             f.write('No index html for this web site')
        except urllib.error.URLError:
             f = open('/home/jnejati/page_speed/inline_output/' + self.s1.netloc, 'w+')
             f.write('No index html for this web site')
        except UnicodeDecodeError:
             f = open('/home/jnejati/page_speed/inline_output/' + self.s1.netloc, 'w+')
             f.write('No index html for this web site')
        except:
             e = sys.exc_info()[0]
             f = open('/home/jnejati/page_speed/inline_output/' + self.s1.netloc, 'w+')
             f.write( "<p>Error: %s</p>" % e )



