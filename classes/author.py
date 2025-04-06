


# author or translator? same data, same class

# to do: allow aliases, and if for two auths
# if any names match, and birth matches, it's a match

from classes.paths import paths

# Don't import TitleSet: circular-- see note above "addBook"
# from classes.titleSet import titleSet


class author: 
    def __init__(self):
        self.gutenId = " "
        self.lastname = " "
        self.othernames = " "
        self.birth = " "
        self.death = " "
        self.workIds = [] 
        self.books = []
        self.isTranslator = False
        self.wikiLink = " "
        self.name = " "
        self.tag = " "


    # used by below: give a list of bad and corresponding good, 
    # replace characters in bad!= corresponding good, when they occur in "str"
    def filterString(self, victim, bad, good):
        newStr = victim; 
        for i in range(0, len(bad)):
            if (bad[i]!=good[i]):
                newStr = newStr.replace(bad[i], good[i]) 
        return newStr

    def safe(self, inStr):
        problematics =   " !\"#$%&'()*+,-._0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~€‚ƒ„…†‡ˆ‰Š‹ŒŽD‘’“”•–—˜™š›œžŸ¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ\n\t"
        parochials     =  " I XSPA CDXT -  0123456789  CEDPAABCDEFGHIJKLMNOPQRSTUVWXYZ   A  ABCDEFGHIJKLMNOPQRSTUVWXYZCIDNE F  TTAOSCOZD    X  SXSDOZYJSSOYIS CA -R OT23 UG  10D424PAAAAAAACEEEEIIIIDNOOOOOXOUUUUYBBAAAAAAACEEEEIIIIDNOOOOODOUUUUYBY  "
        return self.filterString(inStr, problematics, parochials)

    def readline(self, ln):
        wds = ln.split(",")
        self.gutenId = wds[1]
        self.birth = wds[2]
        self.death = wds[3]
        self.isTranslator = (wds[4] == "True")
        self.wikiLink = wds[5] 
        self.lastname = wds[6]
        pl = len(wds[0])+1 +len(wds[1])+1 +len(wds[2])+1 +len(wds[3])+1 +len(wds[4])+1 +len(wds[5])+1 +len(wds[6])+1
        self.othernames = ln[pl:]
        self.finish()

    def writeline(self):
        ln = "A," + self.gutenId + "," + self.birth + "," + self.death + ","
        ln = ln + str(self.isTranslator) + "," + self.wikiLink + ","
        ln = ln + self.lastname + "," + self.othernames + "\n"
        return ln


    # in lieu of looking up titles in something, the F_authors pass keeps a
    # list of all authors and adds titles to them as encountered.
    # expected format of this is a string, 'html_book_link + &&& + gid + &&& + book_title'
    # really, that second thing is just a string for the link
    def addBook(self, gid, bkLine): 
        self.workIds.append(gid)
        self.books.append(bkLine)

    def finish(self): 
        self.name = self.lastname + "," + self.othernames
        self.tag = self.safe(self.lastname[0:6]) + self.gutenId

    # for my cat, root/authors/index.html
    #             root/authors/firstLetter/index.html
    #             root/authors/firstLetter/lastname.html
    def htmlDir(self):
        return "/authors/" + self.tag[0:1] + "/"

    def htmlPath(self):
        return "/authors/" + self.tag[0:1] + "/" + self.tag + ".html"

    def matches(self, other):
        if (self.gutenId == other.gutenId):
            if (self.gutenId!="-1"): 
                return True
        if (self.lastname != other.lastname):
            return False
        if (self.othernames != other.othernames):
            return False
        return False

    def lessThan(self, other):
        return self.tag < other.tag

    def duplicate(self):
        res = author()
        res.gutenId = self.gutenId
        res.lastname = self.lastname
        res.othernames = self.othernames
        res.birth = self.birth
        res.death = self.death
        for id in self.workIds:
            res.workIds.append(id)
        res.isTranslator = self.isTranslator
        res.finish()
        return res

    def report(self):
        print("athrp:" + self.tag + "--" + self.name + "--" + self.birth)


    def makeHTML(self, paths):
        htpt = paths.finalTarget + self.htmlPath()
        # print("making auth page at " + htpt)
        file = open(htpt, "w") 
        file.write('<!DOCTYPE html ><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />')
        file.write('<link rel="stylesheet" href="../../styles.css"><body><title>Auth:' + self.tag)
        file.write('</title></head><body><div class="container">')
        file.write('<div class="rowbox"><div class="left"><img src="../../authors.jpg"/></div>')
        file.write('<div class="right"><br><br>Author Page for <b>' + self.name)
        file.write('</b> (' + str(self.birth) + "-" + str(self.death) + ')<br>')
        if (self.wikiLink != " "):
            file.write('<a href="' + self.wikiLink + '">page at wikipedia</a><br>')
        file.write('</div><div class="clear"></div></div><div class="rowbox"><div class="left">')
        file.write('<img src="../../titles.jpg"/></div><div class="right">')
        for bid in self.books:
            words = bid.split('&&&')
            file.write('<a href="../../' + words[0] + '">' + words[1] + '</a>: ' + words[2] + '</br>')
        file.write('</div><div class="clear"></div></div><div></body></html>')
        file.close() 

