__author__ = 'jnejati'
import os
import json
from collections import defaultdict
import numpy as np


def prepare_dataset(orig_jsons, mod_jsons):
    comp_dict = defaultdict(list)
    download_dict = defaultdict(list)
    javascript_type_list = ['application/x-javascript', 'application/javascript', 'application/ecmascript',
                            'text/javascript', 'text/ecmascript', 'application/json', 'javascript/text']
    css_type_list = ['text/css', 'css/text']
    dir_orig = os.listdir(orig_jsons)  # return list of files in path
    dir_modified = os.listdir(mod_jsons)
    for files_orig in dir_orig:
        if files_orig.startswith('original.testbed.localhost') and files_orig.endswith('.json'):
            for files_modified in dir_modified:
                if files_modified.startswith('modified.testbed.localhost') and files_modified.endswith('.json'):
                    files_orig_site = files_orig.replace('original.testbed.localhost_', '')
                    files_modified_site = files_modified.replace('modified.testbed.localhost_', '')
                    if files_orig_site == files_modified_site:
                        files_orig = os.path.join(orig_jsons, files_orig)
                        files_modified = os.path.join(mod_jsons, files_modified)
                        data_orig = open(files_orig)
                        d_orig = json.load(data_orig)
                        data_modified = open(files_modified)
                        d_modified = json.load(data_modified)
                        if len(d_orig) < 5 or len(d_modified) < 5:
                            break
                        if not d_orig['objs'] or not d_orig['deps'] or not d_modified['objs'] or not d_modified['deps']:
                            break
                        if not (len(d_orig['objs']) == len(d_modified['objs'])):
                            break
                        # ##
                        # {sitename:[object, orig_len, cmp_time, new_cmp_time ]}
                        # {sitename:[object, orig_len, dl_receivelast, modified_dl_receive_last ]}
                        ###
                        for i in range(len(d_orig['objs'])):
                            temp_comp_list = []
                            temp_download_list = []
                            if d_orig['objs'][i]['comps'] and d_orig['objs'][i]['download']:
                                if d_orig['objs'][i]['download']['type'] in javascript_type_list or \
                                                d_orig['objs'][i]['download']['type'] in css_type_list:
                                    if d_orig['objs'][i]['url']:
                                        temp_comp_list.append(d_orig['objs'][i]['url'])
                                        temp_download_list.append(d_orig['objs'][i]['url'])
                                        #comp_dict[files_orig_site].append(d_orig['objs'][i]['url'])
                                    else:
                                        continue
                                    if d_orig['objs'][i]['download']['len']:

                                        temp_comp_list.append(d_orig['objs'][i]['download']['len'])
                                        temp_download_list.append(d_orig['objs'][i]['download']['len'])
                                        #comp_dict[files_orig_site].append(d_orig['objs'][i]['download']['len'])
                                    else:
                                        #comp_dict[files_orig_site].append(0)
                                        continue

                                    comp_time_orig = 0
                                    for j in range(len(d_orig['objs'][i]['comps'])):  # Goes through all of the comps
                                        if d_orig['objs'][i]['comps'][j]['time'] < 0:
                                            print("Negative time in")
                                            print(d_orig['objs'][i]['comps'][j]['id'])

                                        else:
                                            comp_time_orig = comp_time_orig + d_orig['objs'][i]['comps'][j]['time']

                                    temp_comp_list.append(comp_time_orig)

                                    download_time_orig = 0

                                    if d_orig['objs'][i]['download']['receiveLast'] < 0:
                                      print("Negative time/length in")
                                      print(d_orig['objs'][i]['download']['id'])
                                    else:
                                        download_time_orig = download_time_orig + d_orig['objs'][i]['download']['receiveLast']
                                    temp_download_list.append(download_time_orig)
                                    #comp_dict[files_orig_site].append(time_orig)
                                    for k in range(len(d_modified['objs'])):
                                            if (d_modified['objs'][k]['url'] == d_orig['objs'][i]['url'] or d_modified['objs'][k]['url'].replace('http://modified.testbed.localhost/', '') == d_orig['objs'][i]['url'].replace('http://original.testbed.localhost/', '')) or d_modified['objs'][k]['url'].replace('modified.testbed.localhost', '') == d_orig['objs'][i]['url'].replace('original.testbed.localhost', '') or d_modified['objs'][k]['url'].replace('modified.testbed.localhost%2F:', '') == d_orig['objs'][i]['url'].replace('original.testbed.localhost%2F:', '' ):
                                                if d_modified['objs'][k]['download']['type'] in javascript_type_list or \
                                                                d_modified['objs'][k]['download']['type'] in css_type_list:
                                                    #print(d_modified['objs'][k]['url'])
                                                    comp_time_modified = 0
                                                    download_time_modified = 0
                                                    for l in range(len(d_orig['objs'][i]['comps'])):  # Goes through all of the comps
                                                        if d_modified['objs'][k]['comps'][l]['time'] < 0:
                                                            print("Negative time/length in")
                                                            print(d_modified['objs'][k]['comps'][l]['id'])

                                                        elif d_modified['objs'][k]['comps'][l]['time']:
                                                            comp_time_modified = comp_time_modified + d_modified['objs'][k]['comps'][l][
                                                                'time']
                                                            #print(d_modified['objs'][k]['url'], "time_modified", time_modified)
                                                    temp_comp_list.append(comp_time_modified)

                                                    if d_modified['objs'][k]['download']['receiveLast'] < 0:
                                                        print("Negative time/length in")
                                                        print(d_orig['objs'][i]['download']['id'])
                                                    elif d_modified['objs'][k]['download']['receiveLast']:
                                                        download_time_modified = download_time_modified + d_modified['objs'][k]['download']['receiveLast']
                                                    temp_download_list.append(download_time_modified)


                                                    comp_dict[files_orig_site].append(temp_comp_list[0])
                                                    comp_dict[files_orig_site].append(temp_comp_list[1])
                                                    comp_dict[files_orig_site].append(temp_comp_list[2])
                                                    comp_dict[files_orig_site].append(temp_comp_list[3])
                                                    #comp_dict[files_orig_site].append(time_modified)

                                                    download_dict[files_orig_site].append(temp_download_list[0])
                                                    download_dict[files_orig_site].append(temp_download_list[1])
                                                    download_dict[files_orig_site].append(temp_download_list[2])
                                                    download_dict[files_orig_site].append(temp_download_list[3])

    print('---------------------------------------------------------------------------------')
    # print(comp_dict.values())
    a = comp_dict.values()
    b = download_dict.values()
    comp_array_list = []
    download_array_list = []

    for comp_lists in a:
        for i in range(0, len(comp_lists), 4):
            try:
                comp_array_list.append([ comp_lists[i + 1], comp_lists[i + 2], comp_lists[i + 3]])
            except IndexError:
                print("exception:", comp_lists[i-1], comp_lists[i], comp_lists[i+1] )
                break
    for download_lists in b:
        for i in range(0, len(download_lists), 4):
            try:
                download_array_list.append([ download_lists[i + 1], download_lists[i + 2], download_lists[i + 3]])
            except IndexError:
                print("exception:", download_lists[i-1], download_lists[i], download_lists[i+1] )
                break
    print(comp_array_list)
    #print(download_array_list)
    comp_array_list = np.array(comp_array_list)
    download_array_list = np.array(download_array_list)

    #print(download_array_list.shape)
    return comp_array_list , download_array_list
    #files = os.path.join(orig_jsons, files)


"""open orig and modified, for each json file, build two  dictionaries:
     {sitename:[object,orig_len, dl_receivelast,modified_dl_receive_last ]}
     {sitename:[object,orig_len, cmp_time, new_cmp_time ]}
the first 3 features are our training data and the last one is the target.
 "objs" : [
      {
         "when_comp_start" : 1,
         "url" : "http://cinamon.cs.stonybrook.edu/",
         "id" : "r1",
         "comps" : [
            {
               "s_time" : 41.6289999848232,
               "time" : 0.812000012956496,
               "type" : "evalhtml",
               "id" : "r1_c1",
               "e_time" : 42.4409999977797
            }
         ],
         "download" : {
            "receiveFirst" : 2,
            "len" : 66,
            "dns" : 0,
            "dnsEnd" : -1,
            "receiveHeadersEnd" : 7,
            "sslEnd" : -1,
            "connectEnd" : 5,
            "connectStart" : 0,
            "id" : "download_0",
            "receivedTime" : "9.83599992468953",
            "sslStart" : -1,
            "dnsStart" : -1,
            "receiveLast" : 2.83599992468953,
            "s_time" : 0,
            "sendEnd" : 5,
            "sendStart" : 5,
            "type" : "text/html"
         }


"""


"""def main():
    # if (prepare_dataset('./data/desktop_4G_top200_orig_minification/graphs', './data/desktop_4G_top200_modified_minification/graphs')):
    (prepare_dataset('./data/orig', './data/modified'))

if __name__ == '__main__':
    main()"""