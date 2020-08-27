#!/usr/bin/python

import itertools


with open("build_params.txt","r") as f:
    parameters = [param.replace("\n","") for param in f.readlines()]
    with open("build_params.conf", "w") as f:
        for t_size in [1,2]:
            counter=0
            for t_set in itertools.combinations(parameters,t_size):
                f.write("_".join(["t"+str(t_size), "c"+str(counter)])+";"+" ".join(t_set)+"\n")
                counter+=1
