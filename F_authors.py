import csv
import os
import shutil 

# Step 6: scan the tree of all books, make a list of 
# all authors, correlate so that each author has all his/her books
# then make one author page for each. 


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
        sz = 0
        desired = 0
        if (rec.exists and rec.libAccept):
            sz = rec.txtSz
            desired = 1
            for t in rec.subjects:
                print("topic: " + t) # add topic? hmm
            self.bookList.add(rec)
            self.theTree.addBook(rec)
            for aut in rec.auths:
                self.authorSet.add(aut, gbIDStr)
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


    def buildCats(self):
        (a, p, t) = self.recurseDir(self.thePaths.txtTree, "", 0,0,0)
        print("accepted:" + str(a) + " processed:" + str(p) + " totalSz:" + str(t))


    def makeHTML(self):
        self.theTree.finishTopics()
        self.theTree.makeHTML(str(self.bookList.count()))  # fills "subjects"
        # self.bookList.makeGIDHTML() isn't next line filling "titles"?
        self.bookList.makeTitleHTML()
        # self.bookList.makeBookList() isn't prev line filling "titles"?
        self.authorSet.makeHTMLs(self.bookList)  # fills "authors"
        self.authorSet.makeAuthorList()  # ??? stats-gathering?


               
print("defined")

# everything defines ok; run it
def main():
    lb = library()
    lb.buildCats()
    lb.makeHTML()

if __name__ == "__main__":   
    main() 

print("ok then")