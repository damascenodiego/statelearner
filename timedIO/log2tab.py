#!/usr/bin/python

import sys, getopt, re

reset_re = re.compile("^INFO: Step Reset: \\[([0-9]+)\\]")
timedIO_re = re.compile("^INFO: Step TimedIO: \\[([0-9]+)\\]\t([\\w\\.]+)\t/\t([\\w\\.]+)")


def main(argv):
    input_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile="])
    except getopt.GetoptError:
        print('log2tab.py -i <input_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('log2tab.py -i <input_file>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
            output_file = re.sub("\\.log$","",arg)+".tab"
    _in = open(input_file, "r")
    _out = open(output_file, "w")
    _out.write("ResetId\tSymbolId\tOpType\tDuration\tInput\tOutput")
    _out.write("\n")

    line = _in.readline()
    id_reset = -1
    id_iosym = -1
    while line:
        rst_f = reset_re.findall(line)
        tio_f = timedIO_re.findall(line)

        if len(rst_f) != 0:
            id_reset += 1
            id_iosym = -1
            _out.write(str(id_reset) + "\t" + str(id_iosym) + "\t" + "Reset" + "\t" + rst_f[0] + "\t" + "Reset" + "\t" + "Reset")
            _out.write("\n")
        elif len(tio_f) != 0:
            id_iosym += 1
            tio = tio_f[0]
            _out.write(str(id_reset) + "\t" + str(id_iosym) + "\t" + "TimedIO" + "\t" + tio[0] + "\t" + tio[1] + "\t" + tio[2])
            _out.write("\n")
        # _out.write(line)
        line = _in.readline()


if __name__ == "__main__":
    main(sys.argv[1:])
