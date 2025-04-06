import csv
import os
import shutil 

# minimum-redos: given a PG-tree of books, with the little csv files
# made by C_treeRecords.py, the first line of those csv files is 
# flags: "F,exists,desired,isDramaPoem,language"
# how we set "desired" is the decision made here, which determines
# library size-- too many, and the lib isn't portable. 

# if the book's language is not EN, FR, or ES, we don't want it. 
# reject if the book's subjects indicate 
#   children's lit
#   periodical
#   not text
#   Punch, Chiarivari, or other such vileness
# accept if
#   author is in the good_auths list
#   author born before 1750 or after 1900-- fucking gb victoriana
#   is drama, philosophy, history, slave narratives

# book is known to exist in the subdir; copy


# sample hodge-podge accept-reject logic below

    def makeFromBigBook(self, fullbook):
        if (fullbook.langOK() and fullbook.scanGBDir()==0):
            for a in fullbook.auths:
                self.authors.append(a.duplicate())
            self.title = fullbook.title
            self.gutenId = fullbook.gutenId
            lcc = ""
            hasLCSH = False
            for s in fullbook.subjects:
                if (s.find("LCC: ")!=-1 and lcc==""):
                    lcc = s[5:]
                if (s.find("LCSH: ")!=-1 ):
                    hasLCSH = True
            if (hasLCSH and lcc!=""):
                self.valid = True
            for s in fullbook.subjects:
                if (s.find("LCC: ")!=-1):
                    lcc = s[5:]
                if (s.find("LCSH: ")!=-1):
                    tpc = lcc + ' ' + s[6:]     # self.topics only contains LCSH strings.
                    self.topics.append(tpc)
                su = s.upper()
                if (su.find("JUVENILE")!=-1):
                    self.valid = False 
                if (su.find("CHILDREN")!=-1):
                    self.valid = False # the adult content is maudlin enough
                if (su.find("PERIODICAL")!=-1):
                    self.valid = False
            thePaths = paths()
            digits = '%05d' % int(self.gutenId)
            self.dir = thePaths.htmlDir + "\\books\\" + digits[0:1] + "\\" + digits[1:3] + "\\" + digits[3:] + "\\"
            self.htmlRelativePath = "books/" + digits[0:1] + "/" + digits[1:3] + "/" + digits[3:] + "/" + "index.html"
            brute = self.title.upper()
            if (len(brute)<1):
                brute = "A"
            alloweds = "ABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890"
            for i in range(0,len(brute)):
                if (len(brute)>i):
                    if (alloweds.find(brute[i])==-1):
                        brute = brute.replace(brute[i], "")            
            words = brute.split(' ')
            okwords = ""
            for w in words:
                if w!="A" and w!="AN" and w!="THE":
                    if len(okwords)>0:
                        okwords = okwords + "_"
                    okwords = okwords + w
            self.brutalTitle = okwords
            self.brutalTitleA = okwords[0:1]
            self.brutalTitleAB = okwords[0:2]
            self.titlePath = thePaths.htmlDir + "\\titles\\" + self.brutalTitleA + '\\' 
            self.bookTag = fullbook.safeFn(fullbook.bookTag())
            # print(self.gutenId, okwords, self.brutalTitleA, self.brutalTitleAB)
            if (self.brutalTitle.find("PUNCHINELLO")!=-1):
                self.valid = False 
            if (self.brutalTitle.find("CHARIVARI")!=-1):
                self.valid = False # seriously: *fuck* those guys
            if (self.brutalTitle.find("MISSIONARY")!=-1):
                self.valid = False 
            if (fullbook.language.find("en")==-1):
                self.valid = False # English only for now



    def makeFromEPub(self, ebookPath):
        if (fullbook.langOK() and fullbook.scanGBDir()==0):
            for a in fullbook.auths:
                self.authors.append(a.duplicate())
            self.title = fullbook.title
            self.gutenId = fullbook.gutenId
            lcc = ""
            hasLCSH = False
            for s in fullbook.subjects:
                if (s.find("LCC: ")!=-1 and lcc==""):
                    lcc = s[5:]
                if (s.find("LCSH: ")!=-1 ):
                    hasLCSH = True
            if (hasLCSH and lcc!=""):
                self.valid = True
            for s in fullbook.subjects:
                if (s.find("LCC: ")!=-1):
                    lcc = s[5:]
                if (s.find("LCSH: ")!=-1):
                    tpc = lcc + ' ' + s[6:]     # self.topics only contains LCSH strings.
                    self.topics.append(tpc)
                su = s.upper()
                if (su.find("JUVENILE")!=-1):
                    self.valid = False 
                if (su.find("CHILDREN")!=-1):
                    self.valid = False # the adult content is maudlin enough
                if (su.find("PERIODICAL")!=-1):
                    self.valid = False
            thePaths = paths()
            digits = '%05d' % int(self.gutenId)
            self.dir = thePaths.htmlDir + "\\books\\" + digits[0:1] + "\\" + digits[1:3] + "\\" + digits[3:] + "\\"
            self.htmlRelativePath = "books/" + digits[0:1] + "/" + digits[1:3] + "/" + digits[3:] + "/" + "index.html"
            brute = self.title.upper()
            if (len(brute)<1):
                brute = "A"
            alloweds = "ABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890"
            for i in range(0,len(brute)):
                if (len(brute)>i):
                    if (alloweds.find(brute[i])==-1):
                        brute = brute.replace(brute[i], "")            
            words = brute.split(' ')
            okwords = ""
            for w in words:
                if w!="A" and w!="AN" and w!="THE":
                    if len(okwords)>0:
                        okwords = okwords + "_"
                    okwords = okwords + w
            self.brutalTitle = okwords
            self.brutalTitleA = okwords[0:1]
            self.brutalTitleAB = okwords[0:2]
            self.titlePath = thePaths.htmlDir + "\\titles\\" + self.brutalTitleA + '\\' 
            self.bookTag = fullbook.safeFn(fullbook.bookTag())
            # print(self.gutenId, okwords, self.brutalTitleA, self.brutalTitleAB)
            if (self.brutalTitle.find("PUNCHINELLO")!=-1):
                self.valid = False 
            if (self.brutalTitle.find("CHARIVARI")!=-1):
                self.valid = False # seriously: *fuck* those guys
            if (self.brutalTitle.find("MISSIONARY")!=-1):
                self.valid = False 
            if (fullbook.language.find("en")==-1):
                self.valid = False # English only for now







def processBook(sourceP, destP, subP, gbIDStr):
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
        sP = "E:\\lessMobile\\gutenbergRecs\\cache\\epub\\" + gbIDStr  + "\\pg" + gbIDStr + ".rdf"
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
                processBook(sourceP, destP, nsPath, aName)
            else:
                recurseDir(sourceP, destP, nsPath)


sourcePath = "E:\\gbg"
destPath   = "E:\\gbg"
recurseDir(sourcePath, destPath, "")


               