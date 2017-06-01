#!/usr/bin/python3
#Given a folder with ecoding, instances and list of instances run IDLV for each instances and
#    find the "hard" rule of encoding

import sys
import os
import re
import numpy as np

import progressbar as pb

PID = os.getpid()

TIMEOUT = 600
MEMOUT = 15 * 1024 * 1024

ENCODING = "encoding.dlv2.asp"
INSTANCES = "instances.list"
OUTDIR = ".out_"
HARDRULEFILE = "hardRules"

PERC = 80
MIN_RULE = 4
MAX_RULE = 4

def getLast(s):
    return s.split("/")[-1]


def runSystemStat(system, encoding, instances, directory):
    errorfile = directory+"/err_stat_"+getLast(instances)+str(PID)
    os.system("perl timeout -t %d -m %d ./%s --gstats %s %s > /dev/null 2> %s" % (TIMEOUT, MEMOUT, system, encoding, instances, errorfile))
    time = TIMEOUT
    file = open(errorfile, "r")
    ruleStat = {}
    for line in file:
        mo = re.match(r'^(\d+)%(.+)(\s+)(\d+)$', line)
        if mo:
            p = mo.group(1)
            i = mo.group(4)
            ruleStat[int(i)] = int(p)
    file.close()
#    os.system("rm %s" % errorfile)
    return ruleStat

def runDir(dir, idlv):
    print("Find hard rules for: %s" % getLast(dir))
    encoding = dir+"/"+ENCODING
    problems = []
    file = open(dir+"/"+INSTANCES,"r")
    for line in file:
        line = line.rstrip()
        problems.append(dir+"/"+line)
    file.close()
    #Take the time
    outdir = dir+"/" + OUTDIR  + str(PID)
    os.system("mkdir %s" % (outdir))
#    file = open(outdir+"/resultTime","w")
#    for p in problems:
#        time = runSystem(idlv, encoding, p, outdir)
#        file.write("%s\t%s\n" % (getLast(p), str(time)))

#   Find hard rules
    rulesStats = []
    i_problem = 1
    pb.printProgressBar(0, len(problems))
    for p in problems:
        rs = runSystemStat(idlv, encoding, p, outdir)
        pb.printProgressBar(i_problem, len(problems))
        i_problem += 1
        keys = [k for k in rs]
        while len(rulesStats) <= max(keys):
            rulesStats.append([])
        for k in rs:
            rulesStats[k].append(rs[k])
    file.close()
    rulesMean = [np.mean(e) for e in rulesStats]
    rMDic = {i: rulesMean[i] for i in range(0, len(rulesMean))}

    hardRules = []
    totRunningTime = 0
    for t in sorted(rMDic.items(), key=lambda x: x[1], reverse=True):
        totRunningTime += t[1]
        hardRules.append(t[0])
        if len(hardRules) >= MAX_RULE:
            break
    hardRulesFile = outdir+"/"+HARDRULEFILE
    file = open(hardRulesFile, 'w')
    for r in hardRules:
        file.write(str(r)+"\n")
    file.close()

def main(idlv, directory):
    directoies = []
    for dir in os.listdir(directory):
        directoies.append(directory+dir)
        if not os.path.isfile("%s/%s/%s" % (directory,dir,ENCODING)):
            print("ERROR encoding in %s not exist" % dir)
            exit(10)
        if not os.path.isfile("%s/%s/%s" % (directory,dir,INSTANCES)):
            print("ERROR instances in %s not exist" % dir)
            exit(10)

    for dir in directoies:
        runDir(dir, idlv)


if __name__ == "__main__":
    idlv = sys.argv[1]
    folder = sys.argv[2]
    if len(sys.argv) > 3:
        MAX_RULE = int(sys.argv[3])
    if folder[-1] != '/':
        folder += '/'
    main(idlv, folder)


