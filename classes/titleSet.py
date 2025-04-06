import os
import sys

from shutil import copyfile
from classes.paths import paths
from classes.treeRec import treeRec
from classes.LOCtree import LOCtree

# collect all books we will use
# make pages for first-letter and first-two letter combos
# that have books in them 


class titleSet:
    def __init__(self):
        self.books = []
        self.thePaths = paths()
        self.firsts = "0123456789_ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # one books array per letter of firsts
        for i in range(0,len(self.firsts)):
            self.books.append([]) 


    def add(self, treeRec):
        fc = self.firsts.find(treeRec.tag[0:1])
        if (fc==-1):
            print("TITLE NOT SORTABLE")
            return
        nbks = len(self.books[fc])
        for i in range(0,nbks):
            ob1 = self.books[fc][i]
            if (treeRec.brutalLessThan(ob1)):
                self.books[fc].insert(i, treeRec.duplicate())
                return
        self.books[fc].append(treeRec.duplicate())


    def count(self):
        sum = 0
        for bl in self.books:
            sum = sum + len(bl)
        return sum


    def makeBookHTML(self, theTree):
        tipt = self.thePaths.finalTarget + "/titles"
        if not os.path.exists(tipt):
            os.makedirs(tipt)

        # make a fragment for the root, linking to used single-letter lists
        tiFrgPt = tipt + "/titleFrag.html"
        tiFrg = open(tiFrgPt, "w")

        fl = len(self.firsts)
        for i in range(0, fl):
            letter = self.firsts[i:i+1]
            bl = self.books[i]
            if (len(bl)>0): # if self has any books
                tiFrg.write('<a href="titles/' + letter + '.html">' + letter + '</a>(' + str(len(bl)) + ') -- ')
        
                letPgPt = tipt + "/" + letter + ".html"
                letPg = open(letPgPt, "w")
                letPg.write('<!DOCTYPE html ><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />')
                letPg.write('<title>Titles:' + letter + '</title><link rel="stylesheet" href="../styles.css">')
                letPg.write('</head><body><div class="container">')
                letPg.write('<div class="rowbox"><div class="left"><img src="../spacer.jpg"/></div>')
                letPg.write('                    <div class="right"><br><br>Titles: ' + letter + '</div> <div class="clear"></div></div>')
                letPg.write('<div class="rowbox"><div class="left"><img src="../subtitles.jpg"/></div>')
                letPg.write('<div class="right">')
                for bk in bl:
                    theTree.crossRef(bk)

                    bkpt = bk.htmlPath()
                    # print("bookpath " + bkpt)
                    if not os.path.exists(bkpt):
                        os.makedirs(bkpt)

                    bkln = bk.bookLine()
                    bkParts = bkln.split('&&&')
                    letPg.write('<a href="../' + bkParts[0] + '">' + bkParts[1] + '</a>:' + bkParts[2] + '<br/>')
                    # print("making book " + bk.gutenId + ":" + bk.title)
                    bk.makeStaticHTMLs(self.thePaths, theTree)

                letPg.write('</div><div class="clear"></div></div></div></body></html>')
                letPg.close() 
        tiFrg.close() 
                



    def makeBookList(self):
        file = open("bookList.txt", "w") 
        for bk in self.books:
            bk.lister(file)
        file.close() 



