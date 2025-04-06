
import os

from classes.paths import paths
from classes.treeRec import treeRec
from classes.LOCsingle import LOCsingle
from classes.LOCdouble import LOCdouble
from classes.LOCtopic import LOCtopic

# the LOCtree contains singles; singles contain doubles and topics, doubles contain topics.
#  topics contain treeRecs-- books. 
# I believe that the OC system is: 
#  -single-letter major subject groups
#    -- some books are given single-letter topics
#  -two-letter subgroups that divide up the singles
#    -- then many textual subjects in the two-letters

# The LOC subject letters are in the "subjects" array in lines of the format "LOC AB"
# The textual subjects are in lines of the format "LCSH XXX"
# There could be multiples of both? If there is no LCC, discard 
# If there is more than one LCC, that's OK; they'd make subject cards for each, 
#   and each one gives the location of the book 
# There are often multiple LCSH lines. 

# Therefore: a full topic is one LCC + one LCSH. LOCTree makes one LOCtopic for each pair; 
# each is inserted into the tree. 
# If there is more than one LCC, bad LCSH pairings might happen. 
# I don't know that I have a way to prevent that. 

# actions: 
# 0) load the LOC topics file, which gives texts describing each one- and two-letter class 
#     (in init)-- make a tree, first depth=first letters of LCCs, second=both
#       this make most of the singles and doubles, though new ones can come in w/ books, 
# 1) accept all offered LCC/LCSH pairs and sort them into the tree, with the
#      third depth being LCSH strings-- don't expect many LCSH to match
# 2) make a fragment for the root page linking to all the single-letter topics 
#      that contain any books. 
# 3) makea web page for each single-letter instances that hold any books, 
#      giving links to the two-letters that have any books.
# 4) make a web page for each two-letter topic list that contains anything 
#      there will be ~300 of these, but we have 20k books, maybe. 
#      Use the two-letters' topics list to make a list in the page of topics and books

# each topic has a unique mark that serves for HTML file names & links. 
# the hash can't be unique until all are known, so call "finish topics" after adding all books
# and before using HTML links

class LOCtree:
    def __init__(self):        
        self.thePaths = paths()
        self.singles = []
        # make all singles and all doubles not in e or f
        file = open(self.thePaths.LOCtxt, "r") 
        lines = file.readlines() 
        for ln in lines:
            if ln[1] == ' ':
                ord = LOCsingle() # the singles precede the doubles in the file, so ord gets made
                ord.initFromLine(ln)
                self.singles.append(ord)
                dub = LOCdouble() # single-letter LCC's contain books
                undLine = ln[0:1] + '_ ' + ln[2:]
                dub.initFromLine(undLine)
                ord.addDouble(dub)
            else: 
                dub = LOCdouble() # double-letter LCC
                dub.initFromLine(ln)
                ord.addDouble(dub)


    # convert book to a LOCtopic (or several)
    # all non-EF topics are created here
    # if there's a matching topic already added, find it and just add the new book to it. 
    def addBook(self, aTreeRec):
        lccs = []
        lcshs = []
        lines = []
        for tp in aTreeRec.subjects: 
            if (tp[0:5]=="LCC: "):
                lcc = tp[5:]
                if (len(lcc)<2):
                    lcc = lcc + "_"
                if (lcc[1:2]==" "):
                    lcc = lcc[0:1] + "_"
                lccs.append(lcc)
            if (tp[0:6]=="LCSH: "):
                lcshs.append(tp[6:])
        for lc in lccs:
            for sh in lcshs: # for each lcc/lcsh pair
                topc = LOCtopic()
                topc.initFromBook(lc, sh, aTreeRec)
                print("addBook: topic " + lc + ":" + sh)
                for sn in self.singles:
                    # singles and doubles will reject topics that don't match them
                    sn.maybeAddTopic(topc)


    def finishTopics(self):
        self.singles.sort(key = lambda x: x.mark)
        for sn in self.singles:
            sn.finishTopics()


    # after finishing, convert the book topics to links
    # for all the books. re-find and fiddle with them all
    def crossRef(self, aTreeRec):
        lccs = []
        lcshs = []
        lines = []
        for tp in aTreeRec.subjects: 
            if (tp[0:5]=="LCC: "):
                lcc = tp[5:]
                if (len(lcc)<2):
                    lcc = lcc + "_"
                if (lcc[1:2]==" "):
                    lcc = lcc[0:1] + "_"
                lccs.append(lcc)
            if (tp[0:6]=="LCSH: "):
                lcshs.append(tp[6:])
        for lc in lccs:
            for sh in lcshs: # for each lcc/lcsh pair
                topc = LOCtopic()
                topc.initFromBook(lc, sh, aTreeRec)
                for sn in self.singles:
                    ln = sn.topicLink(topc)
                    if (ln!="-"):
                        aTreeRec.subLinks.append(ln)


    # the tree's index is the root page, which is hand-coded,
    # so this just makes all the subnode pages. 
    def makeHTML(self):
        subjRoot = self.thePaths.finalTarget + "/subjects/"
        if not os.path.exists(subjRoot):
            os.makedirs(subjRoot)
        subjFragment = subjRoot + "singles.html"
        frag = open(subjFragment, "w") 
        for d in self.singles:
            if (d.bookCount > 0):
                d.addHTML(frag)
                d.makeHTML()
        frag.close()