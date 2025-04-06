import csv
import os
import shutil 

# Step 5: convert all the books you still want to HTML

# This finalizes the sorting of books, obv,
# but also, there are links out to subjects and authors, so, those, too.
# Books will be broken into ~1500line "volumes" (web page scrolling consideration)
# with html wrappers, and HTML-needed escapes for &'s etc

# and if you need subject links in books, you need to know where all the
# subjects are, and if you want to link to authors, eh, you could do 
# that separately, but it's not a lot of bother to do it here 

from classes.paths import paths
from classes.treeRec import treeRec

from classes.titleSet import titleSet
from classes.authorSet import authorSet
from classes.LOCtree import LOCtree



class library: 
    def __init__(self):
        self.thePaths = paths()
        self.bookList = titleSet()
        self.theTree = LOCtree()
        self.authorSet = authorSet()


    def processBook(self, treeP, subP, gbIDStr, accepted, processed, totalSz):
        bookD = treeP + "/" + subP
        rec = treeRec()
        rec.read(bookD, gbIDStr)
        # print(rec.gutenId + "," + str(rec.exists) + "," + str(rec.libAccept))
        sz = 0
        desired = 0
        if (rec.exists and rec.libAccept):
            # print("adding " + rec.title)
            sz = rec.txtSz
            desired = 1
            self.theTree.addBook(rec)
            self.bookList.add(rec)
            bookLine = rec.bookLine()
            for aut in rec.auths:
                self.authorSet.add(aut, gbIDStr, bookLine)
        return (desired, 1, sz)


    # a book-dir contains a .txt file
    def isBookDir(self, path):
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


    def recurseDir(self, treeP, subP, accepted, processed, totalSz):
        currentP = treeP + subP
        # print(str(currentP))
        listing = os.listdir(currentP)
        sumAc = 0; 
        sumPr = 0;
        sumTs = 0;
        for aName in listing:
            aPath = currentP + "/" + aName 
            nsPath = subP + "/" + aName
            if (os.path.isdir(aPath)):
                # print("dir:" + aPath) 
                if (self.isBookDir(aPath)):
                    (newAcc, newProcd, newSz) = self.processBook(treeP, nsPath, aName, accepted+sumAc, processed+sumPr, totalSz+sumTs)
                else:
                    (newAcc, newProcd, newSz) = self.recurseDir(treeP, nsPath, accepted+sumAc, processed+sumPr, totalSz+sumTs)
                sumAc += newAcc
                sumPr += newProcd
                sumTs += newSz
        return (sumAc, sumPr, sumTs)


    # recursion root call
    def buildCat(self):
        (a, p, t) = self.recurseDir(self.thePaths.txtTree, "", 0,0,0)
        print("accepted:" + str(a) + " processed:" + str(p) + " totalSz:" + str(t))
    
    
    def makeHTML(self):
        print("finishing")
        self.theTree.finishTopics()
        print("tree html")
        self.theTree.makeHTML()  # fills "subjects" dir
        print("make books")
        self.bookList.makeBookHTML(self.theTree); # fills "titles"
        print("make authors" )
        self.authorSet.makeHTMLs()  # fills "authors"

               
print("defined")

# everything defines ok; run it
def main():
    lb = library()
    lb.buildCat()
    lb.makeHTML()

if __name__ == "__main__":   
    main() 

print("ok then")