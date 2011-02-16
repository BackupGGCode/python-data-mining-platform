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
    
    def Init(config, nodeName, loadFromFile = False):
        termToId = {}
        idToTerm = {}
        idToDocCount = {}
        classToDocCount = {}

        curNode = config.GetName(nodeName)
        nameTermToId = curNode.GetName("term_to_id").GetValue()
        nameIdToTerm = curNode.GetName("id_to_term").GetValue()
        nameIdToDocCount = curNode.GetName("id_to_doc_count").GetValue()
        nameClassToDocCount = curNode.GetName("class_to_doc_count").GetValue()

        if (loadFromFile):
            

    def ReadDict(dic, filename):
        f = open(filename, "r")
        for line in file:
            line = line.decode("utf-8")
            vec = line.split("\t")
            dic[vec[0]] = vec[1]
        f.close()

    def WriteDict(dic, filename):
        f = open(filename, "w")
        for k,v in dic.iteritems():
            f.write((k + "\t" + v).encode("utf-8"))
        f.close()
