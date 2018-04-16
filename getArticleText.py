#!/usr/bin/python3 -W all
"""
    getArticleText.py: retrieve text of all newspaper articles on a page
    usage: getArticleText.py
    note: reads target data from file db.txt
    20180416 erikt(at)xs4all.nl
"""

import csv
import re
import sys
import time
from urllib.request import urlopen
import xml.etree.ElementTree as ET

ARTICLEURLPATH = "./{http://www.loc.gov/zing/srw/}records/{http://www.loc.gov/zing/srw/}record/{http://www.loc.gov/zing/srw/}recordData/{http://purl.org/dc/elements/1.1/}identifier"
COMMAND = sys.argv.pop(0)
DBFILE = "db.txt"
URLPREFIX = "http://jsru.kb.nl/sru/sru?query=type=artikel+and+page="
URLINFIX1 = "+and+date="
URLINFIX2 = "+and+ppn="
URLPOSTFIX = r"&x-collection=DDD_artikel"

newspaperIds = { "08De Volkskrant":"DDD_artikel" }
ppns = { "08De Volkskrant":"412869594" }

def makeDateId(newspaper,date,pageNbr): 
    return(newspaper+"\t"+date+"\t"+pageNbr)

def splitDateId(date):
    return(date.split("\t"))

def readDBFile(fileName):
    data = {}
    with open(fileName,"rt",encoding="utf8") as csvFile:
        csvReader = csv.DictReader(csvFile,delimiter='\t')
        lineNbr = 0
        for row in csvReader:
            try: dateId = makeDateId(row["Titel krant"],row["Datum"],row["Paginanummer"])
            except: sys.exit(COMMAND+": missing data on line "+str(lineNbr))
            data[dateId] = True
            lineNbr += 1
        csvFile.close()
    return(data)

def convertDate(date):
    try: day,month,year = date.split("-")
    except: sys.exit(COMMAND+": error processing date "+date)
    if len(day) == 1: day = "0"+day
    if len(month) == 1: month = "0"+month
    return(year+month+day)

def makeUrl(date):
    newspaper,date,pageNbr = splitDateId(date)
    url = URLPREFIX+str(pageNbr)+URLINFIX1+convertDate(date)+URLINFIX2+str(ppns[newspaper])+URLPOSTFIX
    return(url)

def getUrlData(url):
    time.sleep(1)
    return(str(urlopen(url,data=None).read(),encoding="utf-8"))

def getArticleUrls(dateId):
    url = makeUrl(dateId)
    htmlData = getUrlData(url)
    root = ET.fromstring(htmlData)
    articleUrls = []
    for articleUrl in root.findall(ARTICLEURLPATH):
        articleUrls.append(articleUrl.text)
    return(articleUrls)

def getArticleTexts(articleUrls):
    articleTexts = []
    for articleUrl in articleUrls:
        articleTexts.append(getUrlData(articleUrl))
    return(articleTexts)

def makeFileName(dateId):
    newspaper,date,pageNbr = splitDateId(dateId)
    dateId = makeDateId(newspaper,convertDate(date),pageNbr)
    return(re.sub(r"\s",r"-",dateId)+".xml")

def storeArticleTexts(dateId,articleTexts):
    fileName = makeFileName(dateId)
    with open(fileName,"w") as outFile:
        outFile.write("<container>")
        for articleText in articleTexts:
            outFile.write(articleText)
        outFile.write("</container>")
        outFile.close()
    return()

def main(argv):
    data = readDBFile(DBFILE)
    for dateId in data:
        articleUrls = getArticleUrls(dateId)
        articleTexts = getArticleTexts(articleUrls)
        storeArticleTexts(dateId,articleTexts)
    return(0)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
