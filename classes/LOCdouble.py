import os

from classes.paths import paths
from classes.LOCtopic import LOCtopic
from classes.treeRec import treeRec

# one per two-letter LOC classification (or 1+number, for E & F)
class LOCdouble: 
    def __init__(self):  
        self.lcc = 'X'
        self.description = 'uninit description'
        self.link = '--'
        self.path = '--'
        self.topics = []
        self.bookCount = 0


    # line=line from the G_LOCfams.txt file
    # double marks can be 1, 2, or more chars. 
    def initFromLine(self, line):
        spot = line.find(' ')  # the first space is the character after the LCC
        self.lcc = line[0:spot]
        # taken from the LOC file, used only in the web pages to describe
        self.description = line[spot+1:]
        thePaths = paths()
        self.link = self.lcc + ".html"
        self.path = thePaths.finalTarget + "/subjects/" + self.lcc + ".html"
        self.topics = []
        self.bookCount = 0


    # line=line from the G_LOCfams.txt file
    # double marks can be 1, 2, or more chars. 
    def initFromTopic(self, topic):
        print("adding double from topic: " + topic.lcc + ":"+ topic.description)
        self.lcc = topic.lcc
        # taken from the LOC file, used only in the web pages to describe
        self.description = topic.description
        thePaths = paths()
        self.link = self.lcc + ".html"
        self.path = thePaths.finalTarget + "/subjects/" + self.lcc + ".html"
        self.topics = [topic]
        self.bookCount = 0


    def maybeAddTopic(self, tpic):
        if (self.lcc==tpic.lcc):
            for tpc in self.topics:
                if tpc.maybeAddBook(tpic):
                    print("added to topic " + tpc.lcc + ":" + tpc.description + ":" + tpic.books[0])
                    self.bookCount = self.bookCount +1
                    return True
            # not added to existing? append
            self.topics.append(tpic.duplicate())
            print("adding topic (of" + str(len(self.topics)) + ')' + tpic.lcc + ":" + tpic.description + ":" + tpic.books[0])
            self.bookCount = self.bookCount +1
            return True
        return False
    

    # sort topics alphabetically, then
    # ensure that topic marks are unique 
    def finishTopics(self):
        self.topics.sort(key = lambda x: x.description)
        print("finish: " + str(self.bookCount) + " books in " + self.lcc + ":" + self.description)
        for i in range(0, len(self.topics)):
            self.topics[i].finish(i)


    def topicLink(self, tpic):
        if (self.lcc==tpic.lcc):
            for tpc in self.topics:
                ln = tpc.topicLink(tpic)
                if (ln!="-"):
                    return ln
        return "-"


    def makeHTML(self):
        file = open(self.path, "w") 
        file.write('<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />')
        file.write('<link rel="stylesheet" href="../styles.css"><title>' + self.lcc + '</title>')
        file.write('</head><body><div class="container"><div class="rowbox"><div class="left"><img src="../spacer.jpg"/></div>')
        file.write('<div class="right"><b>' + self.lcc + ':' + self.description + ' -- ' + str(self.bookCount) + ' books</b><br>')
        file.write('<a href="' + self.lcc[0:1] + '.html">Up to classification ' + self.lcc[0:1] + '</a>')
        file.write('</div><div class="clear"></div></div>')
        file.write('<div class="rowbox"><div class="left"><img src="../subjects.jpg"/></div><div class="right">')
        file.write('<b>Topics in ' + self.lcc + ':</b></br>')                
        for sn in self.topics:
            sn.addHTML(file)
        file.write('</div><div class="clear"></div></div></div></body></html>')
        file.close()

