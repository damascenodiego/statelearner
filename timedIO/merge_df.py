#!/usr/bin/python3

import sys, getopt
import pandas as pd
import os.path


def main(argv):
    prefix = ''
    file_dir = ''
    config_file = ''
    try:
        opts, args = getopt.getopt(argv, "hp:d:c:", ["prefix=","dir=","configs="])
    except getopt.GetoptError:
        print('merge_df.py -p <prefix> -d <dir> -c <:config file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('merge_df.py -p <prefix> -d <dir> -c <:config file>')
            sys.exit()
        elif opt in ("-p", "--prefix"):
            prefix = arg
        elif opt in ("-d", "--dir"):
            file_dir = arg
        elif opt in ("-c", "--configs"):
            config_file = arg
    if len(prefix) == 0 or len(file_dir) == 0 or len(config_file) == 0:
        print('merge_df.py -p <prefix> -d <dir> -c <:config file>')
        sys.exit(2)

    _cf = open(config_file, "r")
    id_flags = dict()
    set_flags = set()
    for i in _cf.readlines():
        conf_id, conf = i.split(";")
        id_flags[conf_id] = conf.replace("\n","").split(" ")
        for j in id_flags[conf_id]:
            set_flags.add(j)
    _cf.close()

    merged_df = None
    for conf_id,flags in id_flags.items():
        _a_tab = file_dir+"/"+prefix+conf_id+"/"
        if not os.path.exists(_a_tab): continue
        _a_tab = _a_tab + "/tlssul.tab"
        if not os.path.exists(_a_tab): continue
        # print(_a_tab)
        tls_df = pd.read_table(_a_tab)
        tls_df['Config_id'] = conf_id
        for _flag in set_flags:
            tls_df['Flag_'+_flag] = 0
        for _flag in flags:
            _flag = _flag.replace("\n","")
            if not(_flag in tls_df.columns):
                tls_df['Flag_'+_flag] = 1
        if merged_df is None:
            merged_df = tls_df
        else:
            merged_df = pd.concat([merged_df, tls_df])

    merged_df.to_csv("merge_df.tab", sep="\t", encoding='utf-8',index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
