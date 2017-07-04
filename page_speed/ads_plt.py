import os


def main():
    path_orig = '/home/jnejati/page_speed/mobile_wifi-yi_pavan_list_orig_ads/temp_files/'
    path_mod = '/home/jnejati/page_speed/mobile_wifi-yi_pavan_list_modified_ads/temp_files/'
    ouput_set = set()
    dirs_orig = os.listdir(path_orig)  # return list of files in path
    dirs_mod = os.listdir(path_mod)  # return list of files in path
    my_dict = {}
    my_dict_n = {}
    write_file = open(os.path.join('/home/jnejati/page_speed', 'ads_no_ads.txt'), 'w')
    #write_file_n = open(os.path.join('/home/jnejati/page_speed', 'not_worth_to_compress.txt'), 'w')

    for files_orig in dirs_orig:
        for files_mod in dirs_mod:
            files_orig = os.path.join(path_orig, files_orig)
            files_mod = os.path.join(path_mod, files_mod)
            if files_orig.split('/')[-1].split('_')[1]  == files_mod.split('/')[-1].split('_')[1]:
                read_orig = open(os.path.join(path_orig, files_orig), 'r')
                read_mod = open(os.path.join(path_mod, files_mod), 'r')
                print(files_orig, ' and' , files_mod)
                load_orig = 0
                load_mod = 0
                for line1 in read_orig:
                    list1 = line1.split(':')
                    if str(list1[0]) == "load":
                        load_orig = float(list1[1]) * 1000
                for line2 in read_mod:
                    list2 = line2.split(':')
                    if str(list2[0]) == "load":
                        load_mod = float(list2[1]) * 1000

                my_dict[str(files_orig).split("/")[-1].split("_")[1]] = [str(load_orig), str(load_mod), str(load_mod/load_orig)]


    print(my_dict)
    for key, value in my_dict.items():
        write_file.write(key + '\t' +  value[0] + '\t' + value[1] + '\t' + value[2]  + '\n')

    """for key, value in my_dict_n.items():
        write_file_n.write(key + '\t' +  value[0] + '\t' + value[1] + '\t' + value[2]  + '\n')"""

    write_file.close()
    #write_file_n.close()


if __name__ == '__main__':
    main()

