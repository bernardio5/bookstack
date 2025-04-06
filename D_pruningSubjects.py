import csv
import os
import shutil 

# minimum-redos: given a PG-tree of books, with the little csv files
# made by C_treeRecords.py, the first line of those csv files is 
# flags: "F,exists,desired,isDramaPoem,language"
# C_etc.py has already rejected non-english, children's lit, 
#      periodicals, and things that are not text.

# D puts its decision on line "L" of the csv's-- don't change XML data!

# D should accept texts, not reject them-- from known-good authors,
# known-interesting topics-- the default answer is no! 
# D is where we carve multiple libraries 


from classes.paths import paths
from classes.treeRec import treeRec
from classes.author import author


def processBook(treeP, subP, gbIDStr, accepted, processed, totalSz, goodAuths):
    print("looking at " + gbIDStr)
    bookD = treeP + "/" + subP
    csvP = bookD + "/" + gbIDStr + ".csv"
    sz = 0
    desired = 0
    keepers = ["song", "epic", "poetry", "ballad", "drama", "disobedience", "magic", "fantasy", "science", "antiqu", "harvard", "travel", "history", "slave", "philosoph", "pira", "shelf: best books ever"]
    rec = treeRec()
    rec.read(bookD, gbIDStr)
    if (rec.exists and rec.desired):
        for a in rec.auths:
            x=0
            try:
                x = int(a.birth)
            except:
                x=0
            if x<1780:
                rec.libAccept = True
                rec.pretext += " - old"
                sz = rec.txtSz    
                desired = 1
            for ga in goodAuths:
                if ga.matches(a):
                    rec.libAccept = True
                    rec.pretext += " - goodAuth"
                    sz = rec.txtSz
                    desired = 1
        for s in rec.subjects:
            sl = s.lower()
            for k in keepers:
                if (sl.find(k)>-1):
                    rec.libAccept = True
                    rec.pretext += " - " + k 
                    sz = rec.txtSz
                    desired = 1
    if (rec.libAccept):
        rec.write(accepted, processed, totalSz)
        print("accepted:" + gbIDStr + " tot:" + str(totalSz))
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


def recurseDir(treeP, subP, accepted, processed, totalSz, goodAuths):
    currentP = treeP + subP
    listing = os.listdir(currentP)
    sumAc = 0; 
    sumPr = 0;
    sumTs = 0;
    for aName in listing:
        aPath = currentP + "/" + aName 
        nsPath = subP + "/" + aName
        if (os.path.isdir(aPath)):
            # print("dir:" + aPath) 
            if (isBook(aPath)):
                (newAcc, newProcd, newSz) = processBook(treeP, nsPath, aName, accepted+sumAc, processed+sumPr, totalSz+sumTs, goodAuths)
            else:
                (newAcc, newProcd, newSz) = recurseDir(treeP, nsPath, accepted+sumAc, processed+sumPr, totalSz+sumTs, goodAuths)
            sumAc += newAcc
            sumPr += newProcd
            sumTs += newSz
    return (sumAc, sumPr, sumTs)


thePaths = paths()

goodAuths = []
gaFile = thePaths.authorsList
with open(gaFile) as f:
    for ln in f:
        ga = author()
        parts = ln.split(',')
        ga.lastname = parts[0]
        ga.othernames = parts[1]
        goodAuths.append(ga)

(a, p, t) = recurseDir(thePaths.txtTree, "", 0,0,0, goodAuths)
print("accepted:" + str(a) + " processed:" + str(p) + " totalSz:" + str(t))



               