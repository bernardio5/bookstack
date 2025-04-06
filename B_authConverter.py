import csv
import os
from shutil import copyfile
import numpy as np
import random
import sys

# processing step 2: make a list of authors 
# from a crappy text csv I harvested off the internets
from classes.paths import paths


goodNames = []
paths = paths()


def safeString(inStr):
    safe = ""
    problematics =   " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~€‚ƒ„…†‡ˆ‰Š‹ŒŽD‘’“”•–—˜™š›œžŸ¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ\n\t"
    parochials     =  " !'#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~E‚f,…tt^0S‹OZD''''*--~*S>ozYj$$oY|S'ca'-r-o+23'ug-,10>424?AAAAAAACEEEEIIIIDNOOOOOxOUUUUYbBaaaaaaaceeeeiiiidnooooo/ouuuuyby  "
    for i in range(0,len(inStr)):
        ch = problematics.find(inStr[i])
        safe = safe + parochials[ch]
    return safe


# open file as text file
ctr = 0;
file = open(paths.roughList, 'r')
# Read each line in the file
for ln in file:
    ctr = ctr +1
    if (len(ln)>3): 
        ln = safeString(ln)
        names = ln.split(",")
        cured = []
        for name in names:
            if (len(name)>1):
                cured.append(name)
        lastName = cured.pop(-1)
        cured

        # output lines: lastname, other names, full name\n
        fancyLine = lastName + ","

        if (len(cured)==0):
            fancyLine = fancyLine + ","
        else:
            for name in cured:
                fancyLine = fancyLine + name + " "
            fancyLine = fancyLine[:-1] + ","

        for name in cured:
            fancyLine = fancyLine + name + " "
        fancyLine = fancyLine + lastName + "\n"

        if (not(fancyLine in goodNames)): 
            goodNames.append(fancyLine)


goodNames.sort()
ctr=0;
with open(paths.authorsList, 'w') as file:
    for ln in goodNames:
        print(str(ctr) + ":" + ln)
        file.write(ln)
        ctr = ctr+1


