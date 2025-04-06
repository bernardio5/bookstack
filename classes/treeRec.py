import csv
import os
import math
import shutil 
import xml.etree.ElementTree as ET 


# library-building step 3: convert all the XML data into 
# records preprocessed for later steps. 

# given we have a PG tree, with only .txt and .rdf files in it. 
# this loads the rdf and extracts what we want to a CSV.
# brutalized strings are all-caps and ASCII, easier to compare

# there is no class for the xml's bc they only need to be read the once.

# don't save data that can be recomputed instead of reloaded.
# recomputation is faster

from classes.author import author
from classes.paths import paths
 
class treeRec:
    def __init__(self):
        self.exists = False
        self.desired = True 
        self.isDrama = False 
        self.language = "-"
        self.gutenId = "-"
        self.title = " "
        self.tag = " " # terse id, longer than gutenid, more human-readable
        self.auth = author()
        self.auths = []      # authors and translators
        self.subjects = []   # refine: lots of kitchen-sinking
        self.txtName = "-" # name of book's .txt file
        self.txtSz = 0
        self.bookDir = "-" # full DOS path to book's dir
        self.pretext = "-" # why desired is False, if it is. 
        self.libAccept = False # D-pass acceptance
        self.subLinks = []  # "subLCC&&&subIndex&&&subDesc
        
    # if there is no RDF, it's not a book; make a line with just "F,F,F,-"
    def initNull(self, bookD, gbID):
        self.exists = False
        self.bookDir = bookD
        self.gutenId = gbID

    # read and write define the format of the csv
    def read(self, path, gbIDStr):
        self.bookDir = path
        self.gutenId = gbIDStr
        csvP = path + "/" + gbIDStr + ".csv"
        if (os.path.isfile(csvP)):
            with open(csvP, encoding="utf-8") as f:
                for ln in f:
                    lnln = len(ln) - 1
                    ln = ln[0:lnln]
                    wds = ln.split(",")
                    match wds[0]:
                        case "F":
                            self.exists = (wds[1] == "True")
                            self.desired = (wds[2] == "True")
                            self.isDrama = (wds[3] == "True")
                            self.language = wds[4]
                        case "T":
                            self.title = ln[2:]
                            self.maketag()
                        case "A":
                            self.auth = author()
                            self.auth.readline(ln)
                            self.auths.append(self.auth)
                        case "P":
                            self.txtSz = int(wds[1])
                            pl = 2 + len(wds[1]) + 1
                            self.txtName = ln[pl:]
                        case "S": 
                            self.subjects.append(ln[2:])
                        case "J":
                            self.pretext = ln[2:]
                        case "L":
                            self.libAccept = (wds[1] == "True")
        else:
            self.exists = False
            self.reject("no csv")


# flags:    "F,exists,desired,isDramaPoem,language"
# title:    "T,full title"  
# path:     "P,txtFileSz,txt fileName" (not directory)
# authors:  "A,gutenId,born,died,isTranslator,wikipediaLink,fullname"
# --- translators: "R,fullname,born,died,wikipediaLink"
# subjects: "S,text"
# description: "D,txt sz, accepted ct, processed ct, 
# rejection reason: "J,pretext"
# second-pass library inclusion: "L,accepted" -- placeholder for D

    def write(self, accepted, processed, totalSz):
        path = self.bookDir + "/" + self.gutenId + ".csv"
        # print("writing:" + path)
        file = open(path, "w", encoding="utf-8")
        ln = "F," + str(self.exists) + "," + str(self.desired) 
        ln = ln + "," + str(self.isDrama) + "," + self.language + "\n"
        file.write(ln)
        ln = "T," + self.title + "\n"
        file.write(ln)
        ln = "P," + str(self.txtSz) + "," + self.txtName + "\n"
        file.write(ln)
        for auth in self.auths: 
            ln = auth.writeline()
            file.write(ln)
        for sub in self.subjects: 
            ln = "S," + sub + "\n"
            file.write(ln)
        ln = "D," + str(accepted) +","+ str(processed) +","+ str(totalSz) +"\n"
        file.write(ln)
        ln = "J," + self.pretext + "\n"
        file.write(ln)
        ln = "L," + str(self.libAccept) + "\n"
        file.write(ln)
        

    # return false if it's not English, French, or Spanish
    def langOK(self):
        if (self.language == "en"):
            return True
        return False

    # what makes a string bad? 1) it screws up HTML with it's on a page
    # 2) it has \n's that fuck up the csv files 3) it can't be used as a path
    # 4) it can't be 

    # used by below: give a list of bad and corresponding good, 
    # replace characters in bad!= corresponding good, when they occur in "str"
    def filterString(self, victim, bad, good):
        newStr = victim; 
        for i in range(0, len(bad)):
            if (bad[i]!=good[i]):
                newStr = newStr.replace(bad[i], good[i]) 
        return newStr

    # Not HTML safe: &<>"'  
    def htmlSafe(self, inStr):
        problematics =   " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~€‚ƒ„…†‡ˆ‰Š‹ŒŽD‘’“”•–—˜™š›œžŸ¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ\n\t"
        parochials     = " !_#$%+_()--_-._0123456789.._=___ABCDEFGHIJKLMNOPQRSTUVWXYZ[_]^__abcdefghijklmnopqrstuvwxyzCIDNE F  TTAOSCOZD    X  SXSDOZYJSSOYIS CA  R OT23 UG  10D424PAAAAAAACEEEEIIIIDNOOOOOxOUUUUYbBaaaaaaaceeeeiiiidnooooo/ouuuuyby\n\t"
        return self.filterString(inStr, problematics, parochials)


    # Not path-safe:<>:"/\|?*
    def pathSafe(self, inStr):
        problematics =   " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~€‚ƒ„…†‡ˆ‰Š‹ŒŽD‘’“”•–—˜™š›œžŸ¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ\n\t"
        parochials     =  " !_#$%+_()--_-._0123456789.._=___ABCDEFGHIJKLMNOPQRSTUVWXYZ[_]^__abcdefghijklmnopqrstuvwxyzCIDNE F  TTAOSCOZD    X  SXSDOZYJSSOYIS CA  R OT23 UG  10D424PAAAAAAACEEEEIIIIDNOOOOOXOUUUUYBBAAAAAAACEEEEIIIIDNOOOOODOUUUUYBY  "
        return self.filterString(inStr, problematics, parochials)

    def asciiSafe(self, inStr):
        problematics =   " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~€‚ƒ„…†‡ˆ‰Š‹ŒŽD‘’“”•–—˜™š›œžŸ¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ\n\t"
        parochials =     " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~E‚f,.tt^0S‹OZD''\"\"*--~*S>ozYj$$oY|S\"ca\"-r-o+23'ug-,10\"424?AAAAAAACEEEEIIIIDNOOOOOxOUUUUYbBaaaaaaaceeeeiiiidnooooo/ouuuuyby\n\t"
        return self.filterString(inStr, problematics, parochials)

    def asciiCapsLockSortingSafe(self, inStr):
        problematics =   " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~€‚ƒ„…†‡ˆ‰Š‹ŒŽD‘’“”•–—˜™š›œžŸ¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ\n\t"
        parochials     =  " I XSPA CDXT   _0123456789  CEDPAABCDEFGHIJKLMNOPQRSTUVWXYZ   A_ ABCDEFGHIJKLMNOPQRSTUVWXYZCIDNE F  TTAOSCOZD    X  SXSDOZYJSSOYIS CA  R OT23 UG  10D424PAAAAAAACEEEEIIIIDNOOOOOXOUUUUYBBAAAAAAACEEEEIIIIDNOOOOODOUUUUYBY  "
        return self.filterString(inStr, problematics, parochials)


    # tag: for alphabatizing; removes articles
    def maketag(self):
        brute = self.asciiCapsLockSortingSafe(self.title)
        words = brute.split(' ')
        okwords = ""
        for w in words:
            if w!="A" and w!="AN" and w!="THE" and len(w)>0:
                if (len(okwords)>0): 
                    okwords += "_"
                okwords += w
        self.tag = okwords


    ############################################################
    # given a Gb ID and a path to an XML for it, scan that XML
    def readXML(self, bookDir, gbIDStr): 
        self.gutenId = gbIDStr
        self.bookDir = bookDir
        xmlfile = bookDir + "/pg" + gbIDStr + ".rdf"
        tree = ET.parse(xmlfile) # create element tree object 
        root = tree.getroot()  # get root element 
        # print("dir:" + bookDir)
        for rec in root:
            tg = rec.tag.split('}',1)[-1]
            if (tg == "ebook"):
                bookRecs = rec
        for child in bookRecs:
            tg = child.tag.split('}',1)[-1]
            if (tg == "title"):
                if (len(child.text)>1):
                    newStr = child.text
                    self.title = newStr.replace('\n', ' ') # read-write can handle everything else.
                    self.maketag()
                    # print("title:"+ self.title)                  
                else:
                    self.reject("title len == 0")
            if (tg == "bookshelf"):
                for gchild in child[0]:
                    gctg = gchild.tag.split('}',1)[-1]
                    if (gctg == "value"):
                        self.subjects.append("Bookshelf: " + gchild.text)
                        # print("subj (bookshelf):"+ self.subjects[-1])
            if (tg == "subject"):
                subjText = ": "
                for gchild in child[0]:
                    gctg = gchild.tag.split('}',1)[-1]
                    if (gctg == "value"):
                        subjText = subjText + gchild.text
                    if (gctg == "memberOf"):
                        vals = list(gchild.attrib.values())
                        if (len(vals[0])>26):
                            subjText = vals[0][25:] + subjText 
                if (subjText!=": "):
                    self.subjects.append(str(subjText))
            if ((tg == "creator") or (tg == "trl")):
                try:
                    # print("creator")
                    self.auth = author()
                    vals = list(child[0].attrib.values()) 
                    self.auth.gutenId = vals[0][12:]
                    if (tg=="trl"):
                        self.auth.isTranslator = True;
                    for gchild in child[0]:
                        gctg = gchild.tag.split('}',1)[-1]
                        gctx = str(gchild.text)
                        if (gctg == "webpage"):
                            vals = list(gchild.attrib.values())
                            addr = str(vals[0])
                            if (addr.find("en.wiki")>0):
                                self.auth.wikiLink = str(vals[0])
                        if (gctg == "name"):
                            names = gctx.split(",")
                            self.auth.lastname = names[0]
                            self.auth.othernames = gctx[(len(names[0])+1):]
                        if (gctg.find("birthdate")!=-1):
                            self.auth.birth = gctx
                        if (gctg.find("deathdate")!=-1):
                            self.auth.death = gctx
                    # self.auth.report()
                except Exception as e:
                    print("******* author exception: ",e)
                    self.auth.report()
                finally:
                    self.auth.finish()
                    self.auths.append(self.auth)
            if (tg == "language"):
                for gchild in child[0]:
                    gctg = gchild.tag.split('}',1)[-1]
                    if (gctg == "value"):
                        self.language = gchild.text
            if (tg == "type"):
                for gchild in child[0]:
                    gctg = gchild.tag.split('}',1)[-1]
                    if (gctg == "value"):
                        if (gchild.text != "Text"): 
                            self.reject("type is not Text")
                

    def setNoText(self):
        self.exists = False
        self.reject("no text")


    def setText(self, textN, textSz): 
        self.exists = True
        self.txtName = textN 
        self.txtSz = textSz 


    def reject(self, why):
        self.desired = False
        self.pretext = why


    def evaluate(self):
        if (not(self.exists)):
            self.reject("no exist")
            return
        if (not self.langOK()):
            self.reject("wrong language")
            return
        if (len(self.title)<1):
            self.reject("no title")
            return
        if (self.txtName=="-"):
            self.reject("no text")
            return
        if (self.bookDir=="-"):
            self.reject("no dir")
            return
        tu = self.title.upper()
        if (tu.find("PUNCH")!=-1):
            self.reject("PUNCH")
            return
        if (tu.find("CHARIVARI")!=-1):
            self.reject("CHARIVARI")
            return
        if (tu.find("MISSIONARY")!=-1):
            self.reject("MISSIONARY")
            return
        hasLCSH = False
        for s in self.subjects:
            su = s.upper()
            if (su.find("DRAMA")!=-1):
                self.isDrama = True
            if (su.find("POETRY")!=-1):
                self.isDrama = True
            if (su.find("LCSH: ")!=-1 ):
                hasLCSH = True
            if (su.find("MISSIONARY")!=-1):
                self.reject("MISSIONARY")
                return
            if (su.find("JUVENILE")!=-1):
                self.reject("JUVENILE")
                return
            if (su.find("CHILDREN")!=-1):
                self.reject("CHILDREN")
                return
            if (su.find("PERIODICAL")!=-1):
                self.reject("PERIODICAL")
                return
        if (len(self.auths)==0):
            self.auth = author()
            self.auth.gutenId = "99999"
            self.auth.lastname = "Anonymous"
            self.auth.othernames = ""
            self.auth.birth = "0"
            self.auth.death = "31"
            self.auth.finish()
            self.auths.append(self.auth)

    # only compare what is written and read-- 
    #   the rest is computed from these
    def matches(self, it):
        if (self.exists != it.exists):
            return False
        if (self.desired != it.desired):
            return False
        if (self.isDrama != it.isDrama):
            return False
        if (self.language != it.language):
            return False
        if (self.title != it.title):
            return False
        if (self.txtName != it.txtName):
            return False
        ln = len(self.auths)
        if (ln!=len(it.auths)):
            return False
        for i in range(ln):
            if (not(self.auths[i].matches(it.auths[i]))):
                return False
        ln = len(self.subjects)
        if (ln!=len(it.subjects)):
            return False
        for i in range(ln):
            # print("subj:" + str(self.subjects[i]) + "?+=" + str(it.subjects[i]))
            if (self.subjects[i] != it.subjects[i]):
                return False
        return True
        

    def brutalLessThan(self, other): 
        return self.tag < other.tag


    def duplicate(self):
        res = treeRec()
        res.exists = self.exists
        res.desired = self.desired
        res.isDrama = self.isDrama
        res.language = self.language
        res.gutenId = self.gutenId
        res.title = self.title
        res.tag = self.tag
        for a in self.auths:
            res.auths.append(a.duplicate())
        res.subjects = self.subjects.copy()
        res.txtName = self.txtName
        res.txtSz = self.txtSz
        res.bookDir = self.bookDir
        res.pretext = self.pretext
        res.libAccept = self.libAccept
        return res


    def htmlPath(self):
        digits = self.tag
        return "titles/" + digits[0:2] + "/" 

    def htmlVolName(self, which=0):
        whichStr = str(which).zfill(2)
        return self.tag[0:6] + self.gutenId + "_" + whichStr + ".html"

    # line of html to be used to link to this book, by auth and subj pages
    def bookLine(self):
        return self.htmlPath() + self.htmlVolName(0) + '&&&' + self.gutenId + '&&&' + self.title

    # ensure target dir exists. load .txt,
    # convert .txt to html (mostly converting \n's to <br>'s')
    # decide how many volumes to output. call makeVolumeHTML that many times.
    def makeStaticHTMLs(self, aPaths, aSubjects):
        # print("making book " + self.title)
        pt = aPaths.finalTarget + "/" + self.htmlPath()
        # print("putting it at " + pt)
        if not os.path.exists(pt):
            os.makedirs(pt)        
        # load file
        txtPath = self.bookDir + "/" + self.txtName
        fileLines = []
        with open(txtPath) as f:
            for ln in f:
                fileLines.append(ln)
        lineCt = len(fileLines)
        numVols = math.floor(lineCt/1500) +1
        # print(str(lineCt)+ " lines, " + str(numVols) + " vols")
        # text reformatting
        if (self.isDrama):
            # if drama, add <br> to all \n -- <pre>, basically.
            for i in range(0,lineCt):
                aln = fileLines[i].replace("&", "&amp;")
                aln = aln.replace("<", "&lt;")
                aln = aln.replace(">", "&gt;")
                aln = aln.replace('"', "&quot;")
                aln = aln.replace("'", "&#39;")
                aln = aln.replace("\n", "<br>\n")
                fileLines[i] = aln
        else:
            # otherwise, allow reflow
            for i in range(0,(lineCt-1)):
                aln = fileLines[i].replace("&", "&amp;")
                aln = aln.replace("<", "&lt;")
                aln = aln.replace(">", "&gt;")
                aln = aln.replace('"', "&quot;")
                aln = aln.replace("'", "&#39;")
                if (len(aln)<55):
                    aln = aln.replace("\n", "<br>\n")
                fileLines[i] = aln
        for i in range(0,numVols):
            self.makeVolumeHTML(aPaths, numVols, i, fileLines)


    def makeVolumeHTML(self, paths, volCt, whichVol, fileLines):
        # print("writing volume "+ str(whichVol) + " of " + str(volCt))
        volNm = self.htmlVolName(whichVol)
        volPath = paths.finalTarget + "/"+ self.htmlPath() + volNm
        print("vol:" + volPath)
        file = open(volPath, "w") 
        file.write("<!DOCTYPE html><html><head>")
        file.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/>")
        file.write("<link rel=\"stylesheet\" href=\"../../styles.css\">")
        file.write("<title>" + volNm + '</title></head><body><div class="vol"><b>' + self.title + ", v." + str(whichVol) + "</b>, <br>by ")
        if (len(self.auths)>0):
            for i in range(0,len(self.auths)):
                file.write('<a href="../../' + self.auths[i].htmlPath() + '">' + self.auths[i].name + '</a>')
                if (self.auths[i].isTranslator):
                    file.write(" (trns)<br>")
                else:
                    file.write("<br>")
        # buttons
        if (whichVol==0): # links to all subjs and vols in vol0
            file.write("subjs: ")
            for sl in self.subLinks:
                chunks = sl.split('&&&') # 0:LCC 1:index 2:desc
                file.write('<a href="../../subjects/' + chunks[0] + ".html#" + chunks[1])
                file.write('">' + chunks[0] + '#' + chunks[1] + '</a>:' + chunks[2] + '<br>')
            file.write("<br/>In " + str(volCt) + " volume(s): ")
            for i in range(0,volCt-1):
                volNm = self.htmlVolName(i)
                file.write("<a href=\"" + volNm + "\">v." + str(i) + "</a> -- ")
            file.write("<a href=\"" + volNm + "\">v." + str(volCt-1) + "</a><br>")
        else: # links to vols -1, -10, 0, +10, and +1 in all the others
            file.write("<br/> ")
            volNm = self.htmlVolName(whichVol-1)
            file.write("<a href=\"" + volNm + "\">prev</a> ---- ")
            if (volCt>10): 
                if (whichVol>10):
                    volNm = self.htmlVolName(whichVol-10)
                    file.write("<a href=\"" + volNm + "\">v." + str(whichVol-10) + "</a> ---- ") 
            volNm = self.htmlVolName(0)
            file.write("<a href=\"" + volNm + "\">first</a> -- ")
            if (volCt>10): 
                if (whichVol<(volCt-11)): 
                    volNm = self.htmlVolName(whichVol+10)
                    file.write("<a href=\"" + volNm + "\">v." + str(whichVol+10) + "</a>")
            if (whichVol<(volCt-1)): 
                volNm = self.htmlVolName(whichVol+1)
                file.write("<a href=\"" + volNm + "\">next</a> -- ")
        file.write("<br><br>")
        # text
        lineMeasure = math.floor(len(fileLines) / volCt)
        startLine = lineMeasure * whichVol
        endLine = startLine + lineMeasure
        if (endLine > len(fileLines)): 
            endLine = len(fileLines)
        for i in range(startLine,endLine):
            file.write(fileLines[i])   
        file.write("</div></body></html>")
        file.close()
