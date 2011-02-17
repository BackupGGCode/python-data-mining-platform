#save materials produced during data-mining
class PyMining:
    #dict store term -> id
    termToId = {} 
    #dict store id -> term
    idToTerm = {}
    #dict store term -> how-many-docs-have-term
    idToDocCount = {}
    #dict store class -> how-many-docs-contained
    classToDocCount = {}

    #filename of above
    nameTermToId = ""
    nameIdToTerm = ""
    nameIdToDocCount = ""
    nameClassToDocCount = ""

    #isInit
    isInit = False

    #curNode
    curNode = None

    @staticmethod
    def Init(config, nodeName, loadFromFile = False):
        PyMining.termToId = {}
        PyMining.idToTerm = {}
        PyMining.idToDocCount = {}
        PyMining.classToDocCount = {}

        PyMining.curNode = config.GetChild(nodeName)
        PyMining.nameTermToId = PyMining.curNode.GetChild("term_to_id").GetValue()
        PyMining.nameIdToTerm = PyMining.curNode.GetChild("id_to_term").GetValue()
        PyMining.nameIdToDocCount = PyMining.curNode.GetChild("id_to_doc_count").GetValue()
        PyMining.nameClassToDocCount = PyMining.curNode.GetChild("class_to_doc_count").GetValue()

        if (loadFromFile):
            PyMining.__ReadDict(termToId, nameTermToId)
            PyMining.__ReadDict(idToTerm, nameIdToTerm)
            PyMining.__ReadDict(idToDocCount, nameIdToDocCount)
            PyMining.__ReadDict(classToDocCount, nameClassToDocCount)
        
        PyMining.isInit = True
        
    @staticmethod
    def __ReadDict(dic, filename):
        f = open(filename, "r")
        for line in file:
            line = line.decode("utf-8")
            vec = line.split("\t")
            dic[vec[0]] = vec[1]
        f.close()

    @staticmethod
    def __WriteDict(dic, filename):
        f = open(filename, "w")
        for k,v in dic.iteritems():
            #line = (str(k)).decode("utf-8") + (str("\t")).decode("utf-8") + (str(v)).decode("utf-8")
            #f.write((str(k) + str("\t") + str(v)))
            #print str(k)
            print str("\t")
            print str(v)
        f.close()
    
    @staticmethod
    def ReadDict(dic, nodeName):
        if (not PyMining.isInit):
            print "init PyMining before using"
        path = PyMining.curNode.GetChild(nodeName).GetValue()
        PyMining.__ReadDict(dic, path)

    @staticmethod
    def WriteDict(dic, nodeName):
        if (not PyMining.isInit):
            print "init PyMining before using"
        path = PyMining.curNode.GetChild(nodeName).GetValue()
        PyMining.__WriteDict(dic, path)
