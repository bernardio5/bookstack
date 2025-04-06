

import os


#authors dirs is root/authors/first/
#    first contains author pages

from classes.author import author
from classes.paths import paths
from classes.treeRec import treeRec
from classes.titleSet import titleSet


class authorSet:
    def __init__(self):
        self.auths = []
        self.allowed = []
        self.thePaths = paths()
        # list of characters
        self.firsts = "0123456789_ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # one auths array per letter of firsts
        for i in range(0,len(self.firsts)):
            self.auths.append([])
            self.allowed.append([])


    def add(self, aut, gid, bookLine):
        uppr = aut.tag
        fc = self.firsts.find(uppr[0:1])
        if (fc==-1):
            print("AUTHOR NOT SORTABLE")
            return
        # print("sorting " + aut.lastname + " into '" + str(fc) + "'' list of " + str(len(self.auths[fc])) )
        for a in self.auths[fc]:
            if a.matches(aut):
                a.addBook(gid, bookLine)
                # print(aut.lastname + " added " + gid)
                return
        newAut = aut.duplicate()
        newAut.addBook(gid, bookLine)
        ntag = newAut.tag
        nas = len(self.auths[fc])
        for i in range(0,nas):
            ob1 = self.auths[fc][i]
            if (ob1.tag>ntag):
                self.auths[fc].insert(i, newAut)
                # print("inserted " + newAut.lastname)
                return
        self.auths[fc].append(newAut)
        # print('appended new author', newAut.name)


    def makeHTMLs(self):
        pt = self.thePaths.finalTarget + "/authors/"
        if not os.path.exists(pt):
            os.makedirs(pt)
        fl = len(self.firsts)
        for i in range(0, fl):
            letter = self.firsts[i:i+1]
            # ensure that all directories exist
            pt = self.thePaths.finalTarget + "/authors/" + letter + "/"
            if not os.path.exists(pt):
                os.makedirs(pt)
            # make a page for each letter
            pt = self.thePaths.finalTarget + "/authors/" + letter + ".html"
            file = open(pt, "w") 
            file.write('<!DOCTYPE html ><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />')
            file.write('<title>Authors:' + letter + '</title><link rel="stylesheet" href="../styles.css">')
            file.write('</head><body><div class="container">')
            file.write('<div class="rowbox"><div class="left"><img src="../spacer.jpg"/></div>')
            file.write('                    <div class="right"><br><br>Authors: ' + letter + '</div> <div class="clear"></div></div>')
            file.write('<div class="rowbox"><div class="left"><img src="../authors.jpg"/></div>')
            file.write('<div class="right">')
            for at in self.auths[i]:
                if (at.tag.find(letter) == 0):
                    file.write('<a href="' + letter + '/' + at.tag + '.html">' + at.name + '</a><br/>')
            file.write('</div><div class="clear"></div></div></div></body></html>')
            file.close() 
        # make all the author pages
        for letList in self.auths:
            for at in letList:
                at.makeHTML(self.thePaths)


    def loadAllowedAuthors(self):
        with open(csvP, encoding="utf-8") as f:
            for ln in f:
                wds = ln.split(",")
                auth = author()
                auth.gutenId = "-1"
                auth.lastname = wds[1]
                pl = ln.find(wds[1]) + len(wds[1]) + 1
                auth.othernames = ln[pl:]
                alloweds.append(auth)

    
    def hasAllowedAuthor(self, minib):
        for aut in minib.authors:
            tg = aut.authorTag()
            fc = ln[0:1]
            fci = self.firsts.find(fc)
            if (fci==-1):
                return False
            if (tg in self.alloweds[fci]):
                return True
        return False

