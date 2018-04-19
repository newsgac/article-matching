#!/usr/bin/python3 -W all
"""
    xml2db.py: convert xml files with text to db format of erik-fasttext
    usage: xml2db.py file1 [file2 ...]
    note: extracts relevant date from file name
    20180419 erikt(at)xs4all.nl
"""

import nltk
import re
import sys

import xml.etree.ElementTree as ET

COMMAND = sys.argv.pop(0)

def getDate(fileName):
    fields = fileName.split("-")
    year = fields[2][2:4]
    month = fields[2][4:6]
    day = fields[2][6:8]
    return(month+"/"+day+"/"+year)

def readFile(fileName):
    text = ""
    inFile = open(fileName,"r")
    for line in inFile:
        line = re.sub(r"<\?xml[^<>]*>","",line)
        text += line+" "
    inFile.close()
    return(text)

def main(argv):
    for inFile in sys.argv:
        date = getDate(inFile)
        text = readFile(inFile)
        root = ET.fromstring(text)
        for article in root.findall("./text"):
            text = ""
            for child in article: 
                try: text += " "+child.text
                except: continue
            tokenizedSentenceList = nltk.word_tokenize(text)
            tokenizedText = " ".join(tokenizedSentenceList)
            print("__label__UNL DATE="+date+" "+tokenizedText)
    return(0)

if __name__ == "__main__":
    sys.exit(main(sys.argv))

