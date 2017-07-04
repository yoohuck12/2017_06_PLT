__author__ = 'jnejati'
import json
import os
import shutil
import collections
import logging
import tldextract

import glob
from pprint import pprint


class cd:
    """Context manager for changing the current working directory"""

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

order = []  # Array stores the order of boxes
data = []  # Array(List) contains all info about the boxes
dataHash = {}  # Hashtable(Dictionary) used to search for index of the id of boxes.
order_index_lookup = {}
critPath = []
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create console handler and set level to info
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# create error file handler and set level to error
handler = logging.FileHandler(os.path.join('./', "error.log"), "w", encoding=None, delay="true")
handler.setLevel(logging.ERROR)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# create debug file handler and set level to debug
handler = logging.FileHandler(os.path.join('./', "all.log"), "w")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def dataArrives(site_name):
    initial_time = -1
    data_file = open(site_name)
    d = json.load(data_file)
    if len(d) < 5:
        return None
    start_obj = d['start_activity']
    load_obj = d['load_activity']
    if not d['objs'] or not d['deps']:
        return None
    for i in range(len(d['objs'])):
        # print('i', i)
        # print(d['objs'][i])
        obj = {}
        try:
            obj['tag'] = d['objs'][i]['id']
        except KeyError:
            return None

        obj['same_group'] = ''

        try:
            obj['url'] = d['objs'][i]['url']
        except KeyError:
            return None

        obj['same_with'] = ''
        obj['prev'] = []
        obj['next'] = []
        obj['end'] = initial_time

        if d['objs'][i]['download']:
            if d['objs'][i]['download']['receiveLast'] < 0:
                    logger.error("Negative time/length in")
                    logger.error(d['objs'][i]['download']['id'])
                    #obj_download['len'] = 0
                    return None
            else:
                try:
                    temp_input = json.dumps(obj)
                    obj_download = json.loads(temp_input)
                    obj_download['id'] = d['objs'][i]['download']['id']  # ID for the object
                    obj_download['len'] = d['objs'][i]['download']['receiveLast']  # - d.objs[i].download.receiveFirst
                    obj_download['start'] = initial_time
                    obj_download['event'] = 'download'
                    obj_download['bytes'] = d['objs'][i]['download']['len']
                    info = d['objs'][i]['download']['type']
                    s = info.split("/")
                    if s[0] == 'text':
                        obj_download['info'] = s[1] + ":" + s[0]
                    else:
                        obj_download['info'] = s[0] + ":" + s[1]
                    data.append(obj_download)
                except KeyError:
                    return None
        for j in range(len(d['objs'][i]['comps'])):  # Goes through all of the comps
            temp_input = json.dumps(obj)
            obj_comps = json.loads(temp_input)
            obj_comps['start'] = initial_time
            if d['objs'][i]['comps'][j]['time'] < 0:
                logger.error("Negative time/length in")
                logger.error(d['objs'][i]['comps'][j]['id'])
                obj_comps['len'] = 0
            else:
                obj_comps['len'] = d['objs'][i]['comps'][j]['time']

            obj_comps['id'] = d['objs'][i]['comps'][j]['id']
            obj_comps['event'] = ''
            info = d['objs'][i]['comps'][j]['type']
            if info == '1' or info == '2' or info == '3':
                obj_comps['info'] = 'evaljs'
            elif info == '4':
                obj_comps['info'] = 'evalcss'
            else:
                obj_comps['info'] = info
            data.append(obj_comps)
            # all comps in the same objs are sequential (dependent on previous one)
            p = {}
            p['id'] = 'dep_line'
            p['a1'] = data[len(data) - 2]['id']
            p['a2'] = data[len(data) - 1]['id']
            p['time'] = -1
            data[len(data) - 1]['prev'].append(p)

            # Puts id and index into a hash table. Sets id as key, and index as value.
    # print("obj_download_size", len(obj_download), "obj_comp_size", len(obj_comps))

    for i in range(len(data)):
        key_id = data[i]['id']
        dataHash[key_id] = i

        # Goes through all the deps
    for j in range(len(d['deps'])):
        a2 = d['deps'][j]['a2']
        if not a2 in dataHash.keys():
            logging.warning(a2 + ' is in deps but not in objs! Object skipped')
            break

        if (dataHash[a2]):
            index = dataHash[a2]  # Gets the index of a2 in the data_obj
            p = {}  # Creates a new object(dic) to store deps
            p['id'] = d['deps'][j]['id']
            p['a1'] = d['deps'][j]['a1']
            p['a2'] = a2
            if not p['a1'] in dataHash.keys():
                logging.warning(p['a1'] + ' is in deps but not in objs! Object skipped')
                continue
            if (d['deps'][j]['time'] == -1):
                # if time = -1, then a2 starts when a1 finishes
                p['time'] = (data[dataHash[p['a1']]]['len'])
            else:
                p['time'] = d['deps'][j]['time']  # The time that a2 should start after a1
            twice = False
            for k in range(len(data[index]['prev'])):
                if (data[index]['prev'][k]['a1'] == p['a1'] and data[index]['prev'][k]['a2'] == p['a2']):
                    twice = True

            if (not (twice)):
                data[index]['prev'].append(p)  # Puts the deps into the pre array under "a2"
                # we will have a1 ids that a2 depends on, in the prev list of a2
    # Create a next array to record the boxes depends on self.
    for i in range(len(data)):
        for j in range(len(data[i]['prev'])):
            data[dataHash[data[i]['prev'][j]['a1']]]['next'].append(data[i]['prev'][j]['a2'])
    # so far prev and next are filled
    # ##
    # Find out the right start time for each object (if time: -1 ->  back to back, otherwise start from 'time')
    # ##
    done = []
    queue = []
    queue.append(data[dataHash[start_obj]])
    while len(queue) > 0:
        temp = queue.pop()
        # done.append(temp['id'])
        if len(temp['prev']) <= 0:
            temp['start'] = 0
            temp['oStart'] = temp['start']
            done.append(temp['id'])
            for j in range(len(temp['next'])):
                queue.append(data[dataHash[temp['next'][j]]])
        else:
            my_max = 0
            redo = False
            for i in range(len(temp['prev'])):
                p = temp['prev'][i]['a1']
                if not p in done:
                    redo = True
                    break
                time = data[dataHash[p]]['start']
                if (time == -1):
                    break
                if (temp['prev'][i]['time'] == -1):
                    time = time + data[dataHash[p]]['len']
                else:
                    time = time + temp['prev'][i]['time']
                if (time > my_max):
                    my_max = time
            if (not redo):
                temp['start'] = my_max
                temp['oStart'] = temp['start']
                done.append(temp['id'])
                for j in range(len(temp['next'])):
                    if not ((temp['next'][j]) in done):
                        # print("processed", temp['next'][j])
                        queue.append(data[dataHash[temp['next'][j]]])
                        #else: print("skipped", temp['next'][j], done)

    # Find the end time of each box
    for i in range(len(data)):
        data[i]['end'] = data[i]['start'] + (data[i]['len'])

    # Finds the same_group for each box (group of comps and downloads in the same object:i.e same parent id:e.g r1)
    for i in range(len(data)):
        if i != 0:
            tag = data[i - 1]['tag']
            if tag == data[i]['tag']:
                data[i]['same_group'] = data[i - 1]['id']

    # so far prev and next are filled and start and end time are calculated based on the dependency
    # Reorder lines of boxes based on start time

    key = []  # Store the start boxes
    orderhash = {}  # Key - object id, value - start time
    # order = []  #Array stores the order of boxes
    for i in range(len(data)):
        if data[i]['same_group'] == "":
            time = data[i]['start']
            if time not in key:
                key.append(time)
            orderhash[data[i]['id']] = time
    key.sort(key=float)

    # sorted based on start_time

    for i in range(len(key)):
        k = key[i]
        for my_id in orderhash:
            if orderhash[my_id] == k:
                index = dataHash[my_id]
                data_obj = data[index]
                order.append(data_obj)
                if index < (len(data) - 1):
                    index = index + 1
                    current_obj = data[index]
                    while (index < len(data) - 1) and current_obj['same_group'] == data_obj['id']:
                        # above while, was originlly index < len(data)
                        order.append((current_obj))
                        data_obj = current_obj
                        index = index + 1
                        current_obj = data[index]
    # print("Order", order)
    # Puts id and index into a hash table. Sets id as key, and index as value.
    for i in range(len(order)):
        key_id = order[i]['id']
        order_index_lookup[key_id] = i

    critPath.append((order[len(order) - 1]['id'], order[len(order) - 1]['len']))
    critical_path = findCriticalPath(order[len(order) - 1]['prev'])
    if critical_path:
        critical_path.reverse()
        return critical_path

def findCriticalPath(arr):
    if (len(arr) > 0):

        most = 0  # latest end time
        index = 0  # to add to crit path

        # finds latest dependent bar
        for i in range(len(arr)):
            try:
                temp = order[dataHash[arr[i]['a1']]]['end']
            except IndexError:
                return None
            if (temp > most):
                most = temp
                index = i
        critPath.append((arr[index]['a1'], order[order_index_lookup[arr[index]['a1']]]['len']))
        findCriticalPath(order[order_index_lookup[arr[index]['a1']]]['prev'])
        return critPath


def stats(cr_path):
    stats_dic = collections.OrderedDict([
        ('load', 0),
        ('HTMLParse', 0.0),
        ('TTFB', 0.0),
        ('Parse', 0.0),
        ('PostParse', 0.0),
        ('level', 0),
        ('time_download', 0.0),
        ('time_comp', 0.0),
        ('time_block', 0.0),
        ('whatif_matrix', 0.0),
        ('download_blocking', 0.0),
        ('download_proxy', 0.0),
        ('download_dns', 0.0),
        ('download_conn', 0.0),
        ('download_ssl', 0.0),
        ('download_send:', 0.0),
        ('download_receiveFirst', 0.0),
        ('download_receiveLast', 0.0),
        ('parse_style', 0.0),
        ('parse_script', 0.0),
        ('parse_layout', 0.0),
        ('parse_paint', 0.0),
        ('parse_other', 0.0),
        ('parse_undefined', 0.0),
        ('dep_D2E', 0.0),
        ('dep_E2D_html', 0.0),
        ('dep_E2D_css', 0.0),
        ('dep_E2D_js', 0.0),
        ('dep_E2D_timer', 0.0),
        ('dep_RFB', 0.0),
        ('dep_HOL_css', 0.0),
        ('dep_HOL_js', 0.0),
        ('time_download_html', 0.0),
        ('time_download_css', 0.0),
        ('time_download_js', 0.0),
        ('time_download_img', 0.0),
        ('time_download_o', 0.0),
        ('time_block_css', 0.0),
        ('time_block_js', 0.0),
        ('time_ttfb', 0.0),
        ('num_domains_cp', 0.0),
        ('num_domains_all', 0),
        ('text_domains_cp', {}),
        ('text_domains_all', {}),
        ('num_bytes_cp', 0.0),
        ('num_bytes_all', 0.0),
        ('num_send_cp', 0.0),
        ('num_send_all', 0.0),
        ('num_conn_cp', 0.0),
        ('num_conn_all', 0.0),
        ('num_objs_cp', 0.0),
        ('num_objs_all', 0.0),
        ('num_js_cp', 0.0),
        ('num_js_all', 0.0),
        ('num_css_cp', 0.0),
        ('num_css_all', 0.0),
        ('text_domain_tcp_net_cp', []),
        ('text_domain_tcp_net_all', [])
    ])
    javascript_type_list = ['application:x-javascript', 'application:javascript', 'application:ecmascript',
                            'text:javascript', 'text:ecmascript', 'application:json', 'javascript:text']
    css_type_list = ['text/css', 'css:text']

    stats_dic['num_objs_cp'] = str(len(cr_path))
    for cur_index, cur_value in enumerate(cr_path):
        info = order[order_index_lookup[cur_value[0]]]['info']
        if cur_index < len(cr_path) - 1:
            # adding download time on critical path
            next_start = order[order_index_lookup[cr_path[cur_index + 1][0]]]['start']
            cur_start = order[order_index_lookup[cur_value[0]]]['start']
            if next_start >= 0 and cur_start >= 0:
                if order[order_index_lookup[cur_value[0]]]['event'] == 'download':
                    if info.split(":")[0] == 'html':
                        stats_dic['time_download_html'] = stats_dic['time_download_html'] + (next_start - cur_start)
                    elif info.split(":")[0] == 'image':
                        stats_dic['time_download_img'] = stats_dic['time_download_img'] + (next_start - cur_start)
                    elif info in css_type_list:
                        stats_dic['time_download_css'] = stats_dic['time_download_css'] + (next_start - cur_start)
                    elif info in javascript_type_list:
                        stats_dic['time_download_js'] = stats_dic['time_download_js'] + (next_start - cur_start)
                    else:
                        stats_dic['time_download_o'] = stats_dic['time_download_o'] + (next_start - cur_start)

                # adding computation time on critical path
                elif info == 'evalhtml':
                    stats_dic['HTMLParse'] = stats_dic['HTMLParse'] + (next_start - cur_start)
                elif info == 1 or info == 2 or info == 3:  # evaljs
                    stats_dic['parse_script'] = stats_dic['parse_script'] + (next_start - cur_start)
                    #print("next", next_start, "curr", cur_start)
                elif info == 4:  # evalcss
                    stats_dic['parse_style'] = stats_dic['parse_style'] + (next_start - cur_start)
                else:
                    stats_dic['parse_undefined'] = stats_dic['parse_undefined'] + (next_start - cur_start)

            else:
                return None

                # add the end time for the last object in critical path
        elif cur_index == len(cr_path) - 1:
            last_length = order[order_index_lookup[cur_value[0]]]['len']
            if order[order_index_lookup[cur_value[0]]]['event'] == 'download':

                if info.split(":")[0] == 'html':
                    stats_dic['time_download_html'] = stats_dic['time_download_html'] + last_length

                elif info.split(":")[0] == 'image':
                    stats_dic['time_download_img'] = stats_dic['time_download_img'] + last_length

                elif info in css_type_list:
                    stats_dic['time_download_css'] = stats_dic['time_download_css'] + last_length

                elif info in javascript_type_list:
                    stats_dic['time_download_js'] = stats_dic['time_download_js'] + last_length
                else:
                    stats_dic['time_download_o'] = stats_dic['time_download_o'] + last_length
            # computation
            elif info == 'evalhtml':
                stats_dic['HTMLParse'] = stats_dic['HTMLParse'] + last_length

            elif info == '1' or info == '2' or info == '3':  # evaljs
                stats_dic['parse_script'] = stats_dic['parse_script'] + last_length

            elif info == '4':  # evalcss
                stats_dic['parse_style'] = stats_dic['parse_style'] + last_length

            else:
                stats_dic['parse_undefined'] = stats_dic['parse_undefined'] + last_length

    stats_dic['time_download'] = stats_dic['time_download_html'] + stats_dic['time_download_img'] + \
                                 stats_dic['time_download_css'] + stats_dic['time_download_js'] + \
                                 stats_dic['time_download_o']
    stats_dic['time_comp'] = stats_dic['parse_undefined'] + stats_dic['parse_style'] + \
                             stats_dic['parse_script'] + stats_dic['HTMLParse']

    stats_dic['load'] = stats_dic['time_download'] + stats_dic['time_comp']
    return stats_dic


# print('order[order_index_lookup[cr_path[0]]]', order[order_index_lookup[cr_path[0]]])

def post_analyze():
    javascript_type_list = ['application/x-javascript', 'application/javascript', 'application/ecmascript',
                            'text/javascript', 'text/ecmascript', 'application/json', 'javascript/text']
    css_type_list = ['text/css', 'css/text']
    if os.path.isdir('./temp_files/wprof_300_5_pro_1'):
        for root, dirs, l_files in os.walk('./temp_files/wprof_300_5_pro_1'):
            for f in l_files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
    else:
        os.makedirs('./temp_files/wprof_300_5_pro_1')
    path = './graphs'
    dirs = os.listdir(path)  # return list of files in path
    i = 0
    bad_count = 0

    for files in dirs:
        num_objs_all = 0
        num_bytes_all = 0
        num_bytes_cp = 0
        download_dns = 0
        domains_cp = set()
        domains_all = set()
        num_js_cp = 0
        num_js_all = 0
        num_css_cp = 0
        num_css_all = 0

        if files.endswith('.json'):
            files = os.path.join(path, files)
            logger.info("\n" + str(i) + '- Opening ' + files)
            cur_file = open(files)
            try:
                cur_file2 = json.load(cur_file)
            except ValueError:
                logger.error("Error in opening file")
                continue
            num_objs_all = len(cur_file2['objs'])
            c_path = (dataArrives(files))
            for k in range(num_objs_all):
                try:
                    num_bytes_all = num_bytes_all + cur_file2['objs'][k]['download']['len']
                    if cur_file2['objs'][k]['download']['type'] in javascript_type_list:
                        num_js_all += 1
                    elif cur_file2['objs'][k]['download']['type'] in css_type_list:
                        num_css_all += 1
                except KeyError:
                    continue
                domain_name_tuple = tldextract.extract(cur_file2['objs'][k]['url'])
                domain_name = domain_name_tuple.domain + "." + domain_name_tuple.suffix
                domains_all.add(domain_name)
                #Critial Path
                try:
                    if cur_file2['objs'][k]['download']['id'] in [tup[0] for tup in c_path]:
                        num_bytes_cp = num_bytes_cp + cur_file2['objs'][k]['download']['len']
                        download_dns = download_dns + cur_file2['objs'][k]['download']['dns']
                        domains_cp.add(domain_name)
                        if cur_file2['objs'][k]['download']['type'] in javascript_type_list:
                            num_js_cp += 1
                        elif cur_file2['objs'][k]['download']['type'] in css_type_list:
                            num_css_cp += 1
                except TypeError:
                    continue
            if c_path:
                output = stats(c_path)
                output['num_objs_all'] = num_objs_all
                output['num_bytes_all'] = num_bytes_all
                output['num_bytes_cp'] = num_bytes_cp
                output['download_dns'] = download_dns
                output['num_js_cp'] = num_js_cp
                output['num_js_all'] = num_js_all
                output['num_css_cp'] = num_css_cp
                output['num_css_all'] = num_css_all
                output['num_domains_cp'] = len(domains_cp)
                output['num_domains_all'] = len(domains_all)

                logger.info('Analyzing ' + files)
                fname = files.split("/")[-1].split("_.")[0]
                file = open('./temp_files/wprof_300_5_pro_1/' + fname, 'w+')
                if output:
                    for key, value in output.items():
                        file.write(str(key) + ":\t" + str(value) + "\n")
                    logger.info('Critical Path: ')
                    logger.info(c_path)
                    logger.info('Done!')
                else:
                    logger.error('Negative time values! skipping json file')
                file.close()
            else:
                logger.error(str(i) + '- Bad json file: ' + files + ' skipped')
                bad_count += 1
            if c_path: del c_path[:]
            if order: del order[:]
            if data: del data[:]
            if critPath: del critPath[:]
            if dataHash: dataHash.clear()
            if order_index_lookup: order_index_lookup.clear()
        i += 1
    logger.info('------------------------------------------------------------------------------------------')
    logger.info('Total: ' + str(i) + '\nSkipped: ' + str(bad_count) + '\nProcessed: ' + str(i - bad_count))



def run(profile, orig_modified, imp_type):

    graphs_dir = ''
    if orig_modified == 'orig':
            graphs_dir = profile['device_type'] + '_' + profile['conn_type'] + '_' + profile['page_type'] + '_' + 'orig'+ '_' + imp_type
            print('Graphs_Dir:', graphs_dir)
    else:
            graphs_dir = profile['device_type'] + '_' + profile['conn_type'] + '_' + profile['page_type'] + '_' + 'modified' + '_' + imp_type
            print('Graphs_Dir:', graphs_dir)

    with cd(graphs_dir):
        post_analyze()


"""if __name__ == '__main__':
    main()"""
