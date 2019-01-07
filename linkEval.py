#!/usr/bin/env python3
"""
    linkEval.py: evaluate metadata to article text links based on gold data
    usage: linkEval.py -g goldFile -t testFile
    20190107 erikt(at)xs4all.nl
"""

import csv
import getopt
import re
import sys

COMMAND = sys.argv.pop(0)
CSVPATTERN = r"\.csv$"
FIELDARTICLEID = "Artikel ID"
FIELDARTICLETEXT = "Identifier"
FIELDPREDICTION = "Prediction"
NONE = "None"
OPTIONSTRING = "g:t:"
OPTIONG = "-g"
OPTIONT = "-t"
SEPARATORCOMMA = ","
SEPARATORTAB = "\t"

def processArgs(argv):
    goldFileName = ""
    testFileName = ""
    try:
        opts,args = getopt.getopt(argv,OPTIONSTRING)
    except Exception as e:
        sys.exit(COMMAND+": error: "+str(e))
    for opt,arg in opts:
        if opt == OPTIONG: goldFileName = arg
        elif opt == OPTIONT: testFileName = arg
    return(goldFileName,testFileName)

def readDataCsv(fileName):
    data = {}
    try:
        inFile = open(fileName,"r")
        csvReader = csv.DictReader(inFile,delimiter=SEPARATORCOMMA)
        for row in csvReader:
            try: 
                data[row[FIELDARTICLEID]] = row[FIELDARTICLETEXT]
            except Exception as e: 
                sys.exit(COMMAND+": error: "+str(e))
        inFile.close()
    except Exception as e: sys.exit(COMMAND+": error: "+str(e))
    return(data)

def readDataTsv(fileName):
    data = {}
    try:
        inFile = open(fileName,"r")
        csvReader = csv.DictReader(inFile,delimiter=SEPARATORTAB)
        for row in csvReader:
            try: 
                data[row[FIELDARTICLEID]] = row[FIELDPREDICTION]
            except Exception as e: 
                sys.exit(COMMAND+": error: "+str(e))
        inFile.close()
    except Exception as e: sys.exit(COMMAND+": error: "+str(e))
    return(data)

def readData(fileName):
    if re.search(CSVPATTERN,fileName): data = readDataCsv(fileName)
    else: data = readDataTsv(fileName)
    return(data)

def compareData(goldData,testData):
    correct,wrong,noLabel,unknown,missed = 0,0,0,0,0
    for testId in testData:
        if not testId in goldData: unknown += 1
        elif testData[testId] == NONE: noLabel += 1
        elif testData[testId] == goldData[testId]: correct += 1
        else: wrong += 1
    for goldId in goldData:
        if not goldId in testData: missed += 1
    return(correct,wrong,noLabel,unknown,missed)

def printLine(key,total,freq):
    print("{0:11s}".format(key+":"),end="")
    if total == "": print("{0:4s}".format(total),end="")
    else: print("{0:4d}".format(total),end="")
    if freq != "": print(" {0:4.1f}%".format(100.0*freq),end="")
    print("\n",end="")

def printResults(correct,wrong,noLabel,unknown,missed):
    total = correct+wrong+noLabel+unknown
    printLine("articles",total,"")
    printLine("correct",correct,correct/total)
    printLine("wrong",wrong,wrong/total)
    printLine("no label",noLabel,noLabel/total)
    printLine("missed",missed,missed/total)
    printLine("unknown",unknown,unknown/total)
    printLine("precision","",correct/(correct+wrong))
    printLine("recall","",correct/(correct+wrong+noLabel+missed))

def main(argv):
    goldFileName,testFileName = processArgs(argv)
    goldData = readData(goldFileName)
    testData = readData(testFileName)
    correct,wrong,noLabel,unknown,missed = compareData(goldData,testData)
    printResults(correct,wrong,noLabel,unknown,missed)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
