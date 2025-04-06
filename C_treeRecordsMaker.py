import csv
import os
import shutil 

# library-building step 3: convert all the XML data into 
# records preprocessed for our later steps. 

# Given we have a PG tree, with only .txt and .rdf files in it. 
# this loads the rdf and extracts what we want to a CSV.
# The csv shows how well we are parsing the xml,
# which is a point of complexity for the project.
# They also let us gather statistics about final product 
# dimensions.

# flags:    "F,exists,desired,isDramaPoem,language"
# etc! format controlled by pgRec.py

# if there is no RDF, it's not a book; 
#     make a line with just "F,F,F,en"
# same if there's no .txt
# also, do early rejections of non-English, periodicals,
# and children's lit. 

from classes.paths import paths
from classes.treeRec import treeRec


# book is known to exist; process
def processBook(treeP, subP, gbIDStr, accepted, processed, totalSz):
    bookD = treeP + "/" + subP
    pgRecP = bookD + "/pg" + gbIDStr + ".rdf"
    sz = 0
    desired = 0
    # print("xml:"+pgRecP)
    rec = treeRec()
    if (os.path.isfile(pgRecP)):
        print("loading:"+pgRecP)
        rec.readXML(bookD, gbIDStr);
        # there could be two .txt files: ASCII,UTF-8
        # prefer UTF-8.
        listing = os.listdir(bookD)
        toUse = ""
        for aName in listing:
            aPath = bookD + "/" + aName
            # print("maybeUse:" + aName)
            if (os.path.isfile(aPath)):
                # use utf-8 if it's there
                dontUse = 0 # and you can read it
                if (aName.find("-8.txt")>-1):
                    try:
                        with open(aPath) as f:
                            for ln in f:
                                ln2 = ln
                    except: 
                        dontUse = 1 # cant read
                    if (dontUse==0): # did read! use
                        toUse = aName
                # use ASCII otherwise
                else:
                    if ((aName.find(".txt")>-1) and (toUse=="")):
                        try:
                            with open(aPath) as f:
                                for ln in f:
                                    ln2 = ln
                        except: 
                            dontUse = 1
                        if (dontUse==0):
                            toUse = aName
        print("use txt:" + toUse)
        if (toUse==""):
            rec.initNull(bookD, gbIDStr)
        else:
            aPath = bookD + "/" + toUse
            sz = os.path.getsize(aPath)
            rec.setText(toUse, sz)
            rec.evaluate()
    else: # no XML; write null file
        print("no xml")
        rec.initNull(bookD, gbIDStr)
    rec.write(accepted, processed, totalSz)
    # unit test: round-trip data invariance
    # rec2 = treeRec()
    # rec2.read(bookD, gbIDStr)
    # rec2.gutenId += "b"    
    # rec2.write()
    # if (not(rec.compare(rec2))):
    #     print("------------------------------bad round-trip")
    #    exit(0)
    if (rec.exists and rec.desired):
        desired = 1
    else:
        sz = 0
    print("book:" + subP + " sz:" + str(sz)) 
    return (desired, 1, sz)


# a book-dir contains a .txt file
def isBook(path):
    listing = os.listdir(path)
    dirFlag = 0
    bookFlag = False
    for aName in listing:
        if (aName=="0"): # any recursable dirs?
            dirFlag+=1
        if (aName=="1"):
            dirFlag+=1
        if (aName=="2"):
            dirFlag+=1
        if (aName=="3"):
            dirFlag+=1
        if (aName=="4"):
            dirFlag+=1
        if (aName=="5"):
            dirFlag+=1
        if (aName=="6"):
            dirFlag+=1
        if (aName=="7"):
            dirFlag+=1
        if (aName.find(".txt")>-1):
            bookFlag = True
        if (aName.find("-h")>-1):
            bookFlag = True
    if (bookFlag & (dirFlag<2)):
        return True
    return False


def recurseDir(treeP, subP, accepted, processed, totalSz):
    currentP = treeP + subP
    print("dir:" + currentP) 
    listing = os.listdir(currentP)
    sumAc = 0; 
    sumPr = 0;
    sumTs = 0;
    for aName in listing:
        aPath = currentP + "/" + aName 
        nsPath = subP + "/" + aName
        if (os.path.isdir(aPath)):
            print("dir:" + aPath) 
            if (isBook(aPath)):
                (newAcc, newProcd, newSz) = processBook(treeP, nsPath, aName, accepted+sumAc, processed+sumPr, totalSz+sumTs)
            else:
                (newAcc, newProcd, newSz) = recurseDir(treeP, nsPath, accepted+sumAc, processed+sumPr, totalSz+sumTs)
            sumAc += newAcc
            sumPr += newProcd
            sumTs += newSz
    return (sumAc, sumPr, sumTs)

thePaths = paths()
(a, p, t) = recurseDir(thePaths.txtTree, "", 0,0,0)
print("accepted:" + str(a) + " processed:" + str(p) + " totalSz:" + str(t))



               