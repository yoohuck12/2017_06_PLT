__author__ = 'jnejati'
import json
import post_analyze


def classify_deps(file_name):
    ###
    #  Flow dependencies
    ###
    F1_dict = {}   #Loading an object → Parsing the tag that references the object
    F2_dict = {}   #Evaluating an object → Loading the object
    F3_dict = {}   #Parsing the HTML page → Loading the first block of the HTML page*
    F4_dict = {}   #Rendering the DOM tree → Updating the DOM
    F5_dict = {}   #Loading an object referenced by a JavaScript or CSS → Evaluating the JavaScript or CSS*
    F6_dict = {}   #Downloading/Evaluating an object → Listener triggers or timers
    ###
    #  Output dependencies
    ###
    O1_dict = {}   #Parsing the next tag → Completion of a previous JavaScript download and evaluation
    O2_dict = {}   #JavaScript evaluation → Completion of a previous CSS evaluation
    O3_dict = {}   #Parsing the next tag → Completion of a previous CSS download and evaluation
    ###
    #  Binding dependencies
    ###
    B1_dict = {}   #[Lazy] Loading an image appeared in a CSS → Parsing the tag decorated by the image
    B2_dict = {}   #[Lazy] Loading an image appeared in a CSS → Evaluation of any CSS that appears in front of the tag
                   #decorated by the image
    B3_dict = {}   #[Eager] Preloading embedded objects does not depend on the status of HTML parsing. (breaks F1)
    ###
    #  Resource constraint dependencies
    ###
    R1_dict = {}   #Number of objects fetched from different servers → Number of TCP connections allowed per domain
    R2_dict = {}   #Browsers may execute key computational activities on the same thread, creating dependencies among
                   #the activities.This dependency is determined by the scheduling policy.



def show_dependencies(file_name):
    json_orig = open(file_name)
    j_orig = json.load(json_orig)
    for i in range(len(j_orig['deps'])):
        a1 = j_orig['deps'][i]['a1']
        a2 = j_orig['deps'][i]['a2']
        time = j_orig['deps'][i]['time']
        id = j_orig['deps'][i]['id']
        a1_type = ''
        a1_url = ''
        a2_type = ''
        a2_url = ''
        print('id: ', id)
        if a1.startswith('download'):
            for l in range(len(j_orig['objs'])):
                if j_orig['objs'][l]['download']['id'] == a1:
                    a1_url = j_orig['objs'][l]['url']
                    a1_type = j_orig['objs'][l]['download']['type']
        else:
            for i in range(len(j_orig['objs'])):
                for j in range(len(j_orig['objs'][i]['comps'])):
                    if j_orig['objs'][i]['comps'][j]['id'] == a1:
                        a1_url = j_orig['objs'][i]['url']
                        a1_type = j_orig['objs'][i]['comps'][j]['type']

        if a2.startswith('download'):
            for l in range(len(j_orig['objs'])):
                if j_orig['objs'][l]['download']['id'] == a2:
                    a2_url = j_orig['objs'][l]['url']
                    a2_type = j_orig['objs'][l]['download']['type']

        else:
            for i in range(len(j_orig['objs'])):
                for j in range(len(j_orig['objs'][i]['comps'])):
                    if j_orig['objs'][i]['comps'][j]['id'] == a2:
                        a2_url = j_orig['objs'][i]['url']
                        a2_type = j_orig['objs'][i]['comps'][j]['type']

        if a1_type == 1 or a1_type == 2 or a1_type == 3:
                a1_type = 'evaljs'
        elif a1_type == 4:
                a1_type = 'evalcss'
        if a2_type == 1 or a2_type == 2 or a2_type == 3:
                a2_type = 'evaljs'
        elif a2_type == 4:
                a2_type = 'evalcss'
        print('a1: ', a1, 'time:', time,  ' type:', a1_type , ' ', a1_url)
        print('a2: ', a2, 'time:', time,  ' type:', a2_type, ' ', a2_url)
        print('-------------------------------------------------------------------------------------------------------')


def main():
    file_name = './data/orig/original.testbed.localhost_www.bunraku.or.jp_.json'
    show_dependencies(file_name)

if __name__ == '__main__':
    main()
