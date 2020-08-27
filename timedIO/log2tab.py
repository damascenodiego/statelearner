#!/usr/bin/python3

import sys, getopt, re
import pandas as pd
from utils import MealyMachine

reset_re   = re.compile("^\[([0-9\-\ :\.]+)\] \[INFO\] Step Reset: \[([0-9]+)\]")
timedIO_re = re.compile("^\\[([0-9\-\ :\.]+)\\] \[INFO\] Step TimedIO: \\[([0-9]+)\\]\t([\\w\\.]+)\t/\t([\\w\\.]+)")


def main(argv):
    input_file = ''
    output_file = ''
    dot_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:d:", ["ifile=","dfile="])
    except getopt.GetoptError:
        print('log2tab.py -i <input_file> -d <dot file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('log2tab.py -i <input_file> -d <dot file>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
            output_file = re.sub("\\.log$","",arg)+".tab"
        elif opt in ("-d", "--dfile"):
            dot_file = arg
    if len(input_file) == 0 or len(output_file) == 0 or len(dot_file) == 0:
        print('log2tab.py -i <input_file> -d <dot file>')
        sys.exit(2)

    _in = open(input_file, "r")
    _out = open(output_file, "w")
    _out.write("Timestamp\tResetId\tSymbolId\tOpType\tDuration\tInput\tOutput")
    _out.write("\n")
    line = _in.readline()
    id_reset = -1
    id_iosym = -1
    while line:
        rst_f = reset_re.findall(line)
        tio_f = timedIO_re.findall(line)

        if len(rst_f) != 0:
            rst_f=rst_f[0]
            id_reset += 1
            id_iosym = -1
            _out.write(rst_f[0] + "\t" + str(id_reset) + "\t" + str(id_iosym) + "\t" + "Reset" + "\t" + rst_f[1] + "\t" + "Reset" + "\t" + "Reset")
            _out.write("\n")
        elif len(tio_f) != 0:
            id_iosym += 1
            tio = tio_f[0]
            _out.write(tio[0] + "\t" + str(id_reset) + "\t" + str(id_iosym) + "\t" + "TimedIO" + "\t" + tio[1] + "\t" + tio[2] + "\t" + tio[3])
            _out.write("\n")
        # print(line)
        line = _in.readline()
    _in.close()
    _out.close()
    tls_df = pd.read_table(output_file)
    mm = MealyMachine(dot_file)
    tls_df.Duration = tls_df.Duration / 1e+9
    tls_df['Origin'] = mm.list_origin(tls_df.Input.to_list())
    tls_df['ModelOutput'] = mm.list_outputs(tls_df.Input.to_list())
    tls_df['Destination'] = mm.list_destination(tls_df.Input.to_list())

    tls_df.to_csv(output_file, sep="\t", encoding='utf-8', index=False)
    print("File " + output_file + " has been saved!")

    # if tls_df['ModelOutput'].equals(tls_df['Output']):
    #     tls_df.to_csv(output_file, sep="\t", encoding='utf-8', index=False)
    #     print("File "+output_file+" has been saved!")
    # else:
    #     print("ERROR on file "+output_file,file=sys.stderr)
    #     print("There is a mismatch between the Real and the Modeled outputs",file=sys.stderr)
    #     sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
