#!/usr/bin/python3
#Given a folder with ecoding, instances and list of instances run IDLV for each instances and
#    run all encodings and save the running time

import sys
import os
import numpy as np
import datetime

import annotator
import runner

PID = os.getpid()
WARNING_PERC = 30

def extractStats(dir, encoding_means):
    stats = []
    warnings = []
    if 0 not in encoding_means:
        print("ERROR default encoding not in %s" % dir)
        return stats

    problem = runner.getLast(dir)
    base_time = encoding_means[0]
    for e in encoding_means:
        p = ((base_time - encoding_means[e]) / base_time) * 100
        if p > WARNING_PERC:
            warnings.append("%s\t%s\t%s\t%s" % (problem, e, str(encoding_means[e]), str(p)))
        stats.append("%s\t%s\t%s\t%s" % (problem, e, str(encoding_means[e]), str(p)))

    return (stats, warnings)

def main(directory):
    print("Start extract stats")
    directoies = []
    for dir in os.listdir(directory):
        directoies.append(directory+dir)

    dir_out = {}
    for dir in directoies:
        dir_out[dir] =  dir +"/" + annotator.checkDir(dir)

    fileOut = open("result_"+str(datetime.date.today())+"_"+str(PID),"w")
    fileSum = open("result_summary"+str(datetime.date.today())+"_"+str(PID),"w")
    fileOut.write("Problem\tencoding\ttime(s)\t%\n")
    for dir in dir_out:
        do = dir_out[dir]
        file = open(do+"/"+runner.RESULTFILE, "r")
        encoding_times = {}
        for line in file:
            num = int(line.split("\t")[0].split(".")[-1])
            if num not in encoding_times:
                encoding_times[num] = []
            encoding_times[num].append(float(line.split("\t")[2]))
        encoding_means = {}
        for k in encoding_times:
            encoding_means[k] = np.mean(encoding_times[k])

        s, w = extractStats(dir, encoding_means)
        for l in s:
            fileOut.write(l+"\n")
        file.close()
        for l in w:
            fileSum.write(l+"\n")
    fileOut.close()
    fileSum.close()


if __name__ == "__main__":
    folder = sys.argv[1]
    if folder[-1] != '/':
        folder += '/'
    main(folder)
