import csv
import os
import shutil 


# new project code organization: do the processing in passes,
# because this is big data-- achieve definite things per pass,
# but minimize starting over from scratch. 
# Also, don't destroy data, and make processing artifacts for eval.
# For instance, this is step A: convert the 1.2Tb GB data wodge
# + the .05Tb bibliowodge into a single .15Tb text-only wodge. 

from classes.paths import paths

# book is known to exist in the subdir; copy
def copyBook(sourceP, destP, subP, gbIDStr):
    print("book:" + subP) 
    sourceD = sourceP + "\\" + subP
    destD = destP + "\\" + subP
    if (not(os.path.exists(destD))):
        os.makedirs(destD)
    listing = os.listdir(sourceD)
    didCopy = False
    for aName in listing:
        aPath = sourceD + "\\" + aName
        if (os.path.isfile(aPath)):
            filename, file_extension = os.path.splitext(aName)
            if (file_extension==".txt"):
                didCopy = True
                shutil.copyfile(aPath, destD+"\\"+aName)
    if (didCopy): # grab the bibliorec, too
        sP = paths.xmlSet + gbIDStr  + "\\pg" + gbIDStr + ".rdf"
        tP = destD + "\\pg" + gbIDStr + ".rdf"
        if (os.path.isfile(sP)):
            shutil.copyfile(sP,tP)


# a book is a dir contains a .txt file
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


def recurseDir(sourceP, destP, subP):
    currentP = sourceP + "\\" + subP
    listing = os.listdir(currentP)
    for aName in listing:
        aPath = currentP + "\\" + aName 
        nsPath = subP + "\\" + aName
        if (os.path.isdir(aPath)):
            print("dir:" + aPath) 
            if (isBook(aPath)):
                copyBook(sourceP, destP, nsPath, aName)
            else:
                recurseDir(sourceP, destP, nsPath)



paths = new paths()
recurseDir(paths.fullTree, paths.txtTree, "")


               