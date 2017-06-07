#!/usr/bin/python3
#Given a folder with ecoding, instances and list of instances run IDLV for each instances and
#    annotate the encoding

import sys
import os
import analytic
import re

ENCODING = analytic.ENCODING
INSTANCES = analytic.INSTANCES

annotations = [
    "%@rule_ordering(@value=4).",
    "%@rule_ordering(@value=5).",
    "%@rule_projection(@value=0).",
    "%@rule_rewriting_arith().",
    "%@rule_projection(@value=0).\n%@rule_ordering(@value=4).",
    "%@rule_projection(@value=0).\n%@rule_ordering(@value=5).",
    "%@rule_rewriting_arith().\n%@rule_ordering(@value=4).",
    "%@rule_rewriting_arith().\n%@rule_ordering(@value=5)."
]

def checkDir(dir):
    o_dir = ""
    for d in os.listdir(dir):
        if d.startswith(analytic.OUTDIR):
            if len(o_dir) > 0:
                print("Error multiple output directory finded in "+dir)
                exit(10)
            o_dir = d
    if len(o_dir) == 0:
        print("Error no output directory found in "+dir)
        exit(10)
    return o_dir

def getAnnotateEncodings(encoding, hard_rules):
    enc_rules = encoding.split("\n")
    encodings = []
    encodings.append(encoding)
    for ri in hard_rules:
        for a in annotations:
            enc_rules.insert(ri, a)
            e_string = ""
            for l in enc_rules:
                e_string += l + "\n"
            encodings.append(e_string)
            enc_rules.remove(a)
    return encodings


def runDir(dir, o_dir):
    print("Generate encodings for: %s" % dir)
    os.system("rm -rf %s/%s*" % (o_dir, analytic.ENCODING))
    hard_rules = []
    file = open(o_dir+"/"+analytic.HARDRULEFILE,"r")
    for line in file:
        hard_rules.append(int(line.rstrip()))
    file.close()
    with open (dir+"/"+analytic.ENCODING, "r") as myfile:
        encoding = myfile.read()
        encoding = re.sub(r'#show.+\.', '', encoding)
        encoding = re.sub(r'%.+\n', '', encoding)
        encoding = re.sub(r'%\n', '', encoding)
        encoding = encoding.replace("\n", "")
        encoding = encoding.replace(".", ".\n")
        encoding = re.sub(r'\.\n\s+(\[.+\])', r'. \g<1>\n', encoding)
        encodings = getAnnotateEncodings(encoding, hard_rules)
        i = 0
        for e in encodings:
            file = open("%s/%s.%d" % (o_dir, analytic.ENCODING, i),"w")
            file.write(e)
            file.close()
            i += 1


def main(directory):
    directoies = []
    for dir in os.listdir(directory):
        directoies.append(directory+dir)

    dir_out = {}
    for dir in directoies:
        dir_out[dir] =  dir +"/" + checkDir(dir)

    for k in dir_out:
        runDir(k, dir_out[k])





if __name__ == "__main__":
    folder = sys.argv[1]
    if folder[-1] != '/':
        folder += '/'
    main(folder)

