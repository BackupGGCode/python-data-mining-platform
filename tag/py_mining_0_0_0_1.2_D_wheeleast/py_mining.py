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
    #inverse document frequent of termId
    idToIdf = {}

    #filename of above
    nameTermToId = ""
    nameIdToTerm = ""
    nameIdToDocCount = ""
    nameClassToDocCount = ""
    nameIdToIdf = ""

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
        PyMining.idToIdf = {}

        PyMining.curNode = config.GetChild(nodeName)
        PyMining.nameTermToId = PyMining.curNode.GetChild("term_to_id").GetValue()
        PyMining.nameIdToTerm = PyMining.curNode.GetChild("id_to_term").GetValue()
        PyMining.nameIdToDocCount = PyMining.curNode.GetChild("id_to_doc_count").GetValue()
        PyMining.nameClassToDocCount = PyMining.curNode.GetChild("class_to_doc_count").GetValue()
        PyMining.nameIdToIdf = PyMining.curNode.GetChild("id_to_idf").GetValue()

        if (loadFromFile):
            PyMining.__ReadDict(PyMining.termToId, PyMining.nameTermToId, "str", "int")
            PyMining.__ReadDict(PyMining.idToTerm, PyMining.nameIdToTerm, "int", "str")
            PyMining.__ReadDict(PyMining.idToDocCount, PyMining.nameIdToDocCount, "int", "int")
            PyMining.__ReadDict(PyMining.classToDocCount, PyMining.nameClassToDocCount, "int", "int")
            PyMining.__ReadDict(PyMining.idToIdf, PyMining.nameIdToIdf, "int", "float")
        
        PyMining.isInit = True

    @staticmethod
    def Write():
        if (not PyMining.isInit):
            print "call init before write()"
            return False
        PyMining.__WriteDict(PyMining.termToId, PyMining.nameTermToId)
        PyMining.__WriteDict(PyMining.idToTerm, PyMining.nameIdToTerm)
        PyMining.__WriteDict(PyMining.idToDocCount, PyMining.nameIdToDocCount)
        PyMining.__WriteDict(PyMining.classToDocCount, PyMining.nameClassToDocCount)
        PyMining.__WriteDict(PyMining.idToIdf, PyMining.nameIdToIdf)
        return True
        
    @staticmethod
    def __ReadDict(dic, filename, typeK, typeV):
        f = open(filename, "r")
        for line in f:
            line = line.decode("utf-8")
            vec = line.split("\t")
            k = vec[0]
            v = vec[1]
            if (typeK == "int"):
                k = int(k)

            if (typeV == "int"):
                v = int(v)
            elif (typeV == "float"):
                v= float(v)

            dic[k] = v
        f.close()

    @staticmethod
    def __WriteDict(dic, filename):
        f = open(filename, "w")
        for k,v in dic.iteritems():
            if isinstance(k, (str, unicode)):
                f.write(k.encode("utf-8"))
            else:
                f.write(str(k))
            f.write("\t")
            if isinstance(v, (str, unicode)):
                f.write(v.encode("utf-8"))
            else:
                f.write(str(v))
            f.write("\n")
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
