import os

from classes.paths import paths
from classes.treeRec import treeRec

# one per text-described topic in two-letter genus

# Topics are created from book records, but topics can have
# more than one book. From books, topics only need enough
# info to link back to them: link, link text (GBID), and title. 

# topics are created by LOCTree; it gets handed a book, 
# it pulls out LCC and LCSH strings and combines them,
# then makes a topic for each pair and stores them
# Topics are also created by EF singles

# topics don't get their own web pages, so, they make HTML fragments for the
# doubles' pages, and their links are subjects/XX.html#index

class LOCtopic: 
    def __init__(self):
        self.lcc = "XX"
        self.description = "about stuff" # text description from LCSH
        self.index = 0  # place of this topic in parent double's sorted, final list of topics
        # text line, enough to make a link: addr&&&ID&&&title
        self.books = [] # all the books in the topic
        self.link = " "


    def initFromBook(self, dblMark, subj, aTreeRec): 
        self.lcc = dblMark
        self.description = subj
        self.index = 0 
        self.books.append(aTreeRec.bookLine())
        self.link = " "


    def duplicate(self): 
        dupe = LOCtopic()
        dupe.lcc = self.lcc
        dupe.description = self.description
        dupe.index = self.index  
        dupe.books = self.books.copy()
        dupe.link = self.link
        return dupe


    def maybeAddBook(self, tp): 
        if (tp.description==self.description):
            self.books.append(tp.books[0])
            return True
        return False


    def linkString(self):
        return self.lcc + "&&&" + str(self.index) + "&&&" + self.description


    def bookCount(self):
        return len(self.books)


    def finish(self, index):
        self.index = index
        self.link = self.lcc + ".html#" + str(index)


    def topicLink(self, tp): 
        if (tp.description==self.description):
            return self.linkString()
        return "-"


    # topics don't get thier own pages. 
    def addHTML(self, file):
        file.write('<br>Books in topic <b id="' + str(self.index) + '">')
        file.write(self.lcc + '#' + str(self.index) +':' + self.description + '</b><br>')
        for bk in self.books:
            gobs = bk.split('&&&')
            file.write('<a href="../' + gobs[0] + '">' + gobs[1] + '</a>:' + gobs[2] + "<br>")


    # I mean, they used to, but don't call this
    def makeHTML(self, file):
        if not os.path.exists(self.dirPath):
            os.makedirs(self.dirPath)
        htpt = self.dirPath + self.link
        file = open(htpt, "w") 
        file.write('<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />')
        file.write('<link rel="stylesheet" href="../styles.css"><title>' + self.tag)
        file.write('</title></head><body><div class="container"><div class="rowbox">')
        file.write('<div class="left"><img src="../spacer.jpg"/></div><div class="right">')
        file.write('<div class="right">Topic page for: <b>' + self.description + '</b> -- '+  str(len(self.books)) + ' books<br>')
        file.write('Up to classification <a href="' + self.lcc + '.html">' + self.lcc)
        file.write('</div><div class="clear"></a></div></div>')
        file.write('<div class="rowbox"><div class="left"><img src="../subjects.jpg"/></div><div class="right">')
        file.write('<table><tr><td>Book</td><td>Title</td><td>Topic</td></tr>')
        lines = []
        for bk in self.books:
            for tp in bk.subjects:
                if (tp.find(self.lcc)>-1):
                    tpln = tp
            lines.append(tpln + '&&&' + bk.htmlRelativePath + '&&&' + bk.gutenId + '&&&' + bk.title)
        lines.sort()
        for bk in lines:
            (tp, pt, gid, ti) =  bk.split('&&&')
            file.write('<tr><td><a href="' + pt + '">' + gid + '</a></td><td>' + ti + '</td><td>' + tp + '</td></tr>')
        file.write('</table></div><div class="clear"></div></div></div></body></html>')
        file.close() 


