import os

from classes.paths import paths
from classes.treeRec import treeRec
from classes.LOCdouble import LOCdouble


# one per single-letter LOC classification
# contains two-letter classifications and topics

class LOCsingle:
    def __init__(self): 
        self.mark = 'X'
        self.description = 'uninitialized desc'
        self.doubles = [] # list of LOCdoubles in 
        self.path = ' '
        self.link = ' '
        self.bookCount = 0
        

    def initFromLine(self, line): # line=line from the G_LOCfams.txt file
        self.mark = line[0:1]
        self.description = line[2:] # text description of this order
        self.doubles = []
        thePaths = paths()
        self.path = thePaths.finalTarget + "/subjects/" + self.mark + ".html"
        self.link = self.mark + ".html"
        self.bookCount = 0


    def addDouble(self, double): # line from G_LOCfams
        self.doubles.append(double)


    # letters other than E and F have a standard set of 2-letter codes. 
    # E and F are numbered, maybe standard, but not in a helpful way,
    # and maybe we don't have all the two-letter codes! 
    def maybeAddTopic(self, tpic):
        if (tpic.lcc[0:1] == self.mark): # reject if not a match
            for db in self.doubles:
                if db.maybeAddTopic(tpic): # could be an existing double
                    self.bookCount = self.bookCount+1
                    return
            # didn't find one; add it
            d = LOCdouble()
            d.initFromTopic(tpic)
            self.doubles.append(d)
            self.bookCount = self.bookCount+1            

    def finishTopics(self):
        self.doubles.sort(key = lambda x: x.lcc)
        for db in self.doubles:
            db.finishTopics()


    def topicLink(self, tpic):
        if (tpic.lcc[0:1] == self.mark): # reject if not a match
            for db in self.doubles:
                ln = db.topicLink(tpic)
                if (ln!="-"):
                    return ln
        return "-"


    def addHTML(self, frag):
        frag.write('<a href="' + self.link + '">' + self.mark + '</a>(' + str(self.bookCount) + ') --\n')


    def makeHTML(self):
        file = open(self.path, "w") 
        file.write('<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />')
        file.write('<link rel="stylesheet" href="../styles.css"><title>' + self.mark)
        file.write('</title></head><body><div class="container"><div class="rowbox"><div class="left"><img src="../spacer.jpg"/>')
        file.write('</div><div class="right"><br>topic page for <b>' + self.description + '</b><br>')
        file.write('<a href="../index.html">back to library main page</a>')
        file.write('</div><div class="clear"></div></div>')
        file.write('<div class="rowbox"><div class="left"><img src="../subjects.jpg"/></div><div class="right">')
        file.write('<table><tr><td>Subtopic </td><td>Description</td><td># Books</td></tr>')
        for db in self.doubles:
            if (db.bookCount >0):
                db.makeHTML()
                file.write('<tr><td>'+db.lcc+'</td><td><a href="' + db.link + '">')
                file.write(db.description + '</a></td><td>' + str(db.bookCount) +'</td></tr>')
        file.write('</table><table><tr><td>Topic Description</td><td># Books</td></tr>')                
        file.close() 

