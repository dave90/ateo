#!/usr/bin/python3
#Given a folder with ecoding, instances and list of instances run IDLV for each instances and
#    run all encodings and save the running time

import sys
import os
import analytic
import re

import annotator
import progressbar as pb

PID = os.getpid()

TIMEOUT = 600
MEMOUT = 15 * 1024 * 1024

RESULTFILE = "resultTime"

def getLast(s):
    return s.split("/")[-1]


def runSystem(system, encoding, instances, directory):
    errorfile = directory+"/err_time_"+getLast(instances)+str(PID)
    os.system("perl timeout -t %d -m %d ./%s %s %s > /dev/null 2> %s" % (TIMEOUT, MEMOUT, system, encoding, instances, errorfile))
    time = TIMEOUT
    file = open(errorfile, "r")
    for line in file:
        mo = re.search(r'FINISHED CPU (.+?) MEM',line)
        if mo:
            time = float(mo.group(1))
            break
    file.close()
    os.system("rm %s" % errorfile)
    return time


def main(system, directory):
    directoies = []
    for dir in os.listdir(directory):
        directoies.append(directory+dir)

    dir_out = {}
    for dir in directoies:
        dir_out[dir] =  dir +"/" + annotator.checkDir(dir)

    for dir in dir_out:
        print("Run %s" % dir)
        do = dir_out[dir]
        resfile = "%s/%s" % (do, RESULTFILE)
        os.system("rm -rf %s" % resfile)
        file = open(resfile, "w")
        encodings = []
        instances = []
        for f in os.listdir(do):
            if f.startswith(annotator.ENCODING):
                encodings.append(do+"/"+f)
        fileI = open(dir+"/"+annotator.INSTANCES, "r")
        for line in fileI:
            line = line.rstrip()
            instances.append(dir+"/"+line)
        fileI.close()

        tot = len(encodings) * len(instances)
        i_instance = 1
        pb.printProgressBar(i_instance, tot)
        for e in encodings:
            for i in instances:
                time = runSystem(system, e, i, do)
                file.write(getLast(e)+"\t"+getLast(i)+"\t"+str(time)+"\n")
                pb.printProgressBar(i_instance, tot)
                i_instance += 1
        file.close()

if __name__ == "__main__":
    system = sys.argv[1]
    folder = sys.argv[2]
    if folder[-1] != '/':
        folder += '/'

    main(system, folder)

