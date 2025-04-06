

# the conversion project uses data stored in directory trees
# set them here

class paths: 
    def __init__(self):
        #### A_treeCopier step:
        # path to full, 400Gb GB resource tree
        self.fullTree = "D:\\gbg"

        # path to GB XML record set
        self.xmlSet = "E:\\lessMobile\\gutenbergRecs\\cache\\epub"

        # path to txt/xml tree
        # self.txtTree = "/home/zingie/inputs/gbgSm"
        self.txtTree = "/home/zingie/inputs/gbg" # minitree for fast tests

        #### B_ make a list of good authors
        self.roughList = "/home/zingie/nomad/bookstack/B_auths.csv"
        # path to good authors' list
        self.authorsList = "/home/zingie/nomad/bookstack/D_goodAuths.csv"

        #### C_ make csv files for all books; preliminary rejection

        #### D_ further culling; use the author's list

        #### E_ convert desired books to html
        # txt containing Lib of Cong categories and descriptions
        self.LOCtxt = "/home/zingie/nomad/bookstack/G_LOCfams.txt"
        
        # path to final html library
        self.finalTarget = "/home/zingie/nomad/html/library"

