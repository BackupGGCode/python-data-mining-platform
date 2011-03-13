import math
from segmenter import Segmenter
from matrix import Matrix
from py_mining import PyMining
from configuration import Configuration

class ClassifierMatrix:
    def __init__(self, config, nodeName, loadFromFile = False):
        self.node = config.GetChild(nodeName)
        self.segmenter = Segmenter(config, "__segmenter__")
        self.trained = loadFromFile
        PyMining.Init(config, "__global__", loadFromFile)
        
    """
    create train matrix:
        fill dict in PyMining, record:
        1)termToId
        2)idToTerm
        3)termToDocCount
        4)classToDocCount
        and save mat-x using csr, save mat-y using list
    """
    def CreateTrainMatrix(self, path = ""):
        #get input-path
        inputPath = path
        if (inputPath == ""):
            inputPath = self.node.GetChild("train_input").GetValue()

        f = open(inputPath, "r")
        uid = 0
        rows = [0]
        cols = []
        vals = []
        y = []

        #fill the matrix's cols and rows
        for line in f:
            vec = line.split("\t")
            line = vec[0]
            target = int(vec[1])
            y.append(target)
            wordList = self.segmenter.Split(line.decode("utf-8"))

            #store current row's cols
            partCols = []

            #create dicts and fill partCol
            #calculate term-frequent in this loop
            curWordCount = 0
            termFres = {}
            for word in wordList:
                curWordCount += 1
                if (not PyMining.termToId.has_key(word)):
                    PyMining.termToId[word] = uid
                    PyMining.idToTerm[uid] = word
                    uid += 1
                termId = PyMining.termToId[word]
                partCols.append(termId)
                if (not termFres.has_key(termId)):
                    termFres[termId] = 1
                else:
                    termFres[termId] += 1
            #fill partCol
            partCols = set(partCols)
            partCols = list(partCols)
            partCols.sort()

            #fill cols and vals, fill termToDocCount
            for col in partCols:
                cols.append(col)
                #fill vals with termFrequent
                vals.append(termFres[col])
                #fill idToDocCount
                if (not PyMining.idToDocCount.has_key(col)):
                    PyMining.idToDocCount[col] = 1
                else:
                    PyMining.idToDocCount[col] += 1

            #fill rows
            rows.append(rows[len(rows) - 1] + \
                len(partCols))

            #fill classToDocCount
            if (not PyMining.classToDocCount.has_key(target)):
                PyMining.classToDocCount[target] = 1
            else:
                PyMining.classToDocCount[target] += 1

        #fill PyMining's idToIdf
        for termId in PyMining.idToTerm.keys():
            PyMining.idToIdf[termId] = math.log(float(len(rows) - 1) / (PyMining.idToDocCount[termId] + 1))

        #NOTE: now, not mul idf to vals, because not all algorithms need tf * idf
        #change matrix's vals using tf-idf represent
        #for r in range(len(rows) - 1):
        #    for c in range(rows[r], rows[r + 1]):
        #        termId = cols[c]
        #        #idf(i) = log(|D| / |{d (ti included)}| + 1
        #        vals[c] = vals[c] * PyMining.idToIdf[termId]

        #close file
        f.close()

        #write dicts out
        PyMining.Write()

        self.trained = True

        return [Matrix(rows, cols, vals), y] 

    def CreatePredictSample(self, src):
        if (not self.trained):
            print "train Classifier Matrix before predict"
        
        #split sentence
        #if src is read from utf-8 file directly, 
        #    should using CreatePredictSample(src.decode("utf-8"))
        wordList = self.segmenter.Split(src)

        cols = []
        vals = []
        #fill partCols, and create csr
        partCols = []
        termFreqs = {}
        for word in wordList:
            if (PyMining.termToId.has_key(word)):
                termId = PyMining.termToId[word]
                partCols.append(termId)
                if (not termFreqs.has_key(termId)):
                    termFreqs[termId] = 1
                else:
                    termFreqs[termId] += 1
        partCols = set(partCols)
        partCols = list(partCols)
        partCols.sort()
        for col in partCols:
            cols.append(col)
            vals.append(termFreqs[col])

        return [cols, vals]

    """
    create predict matrix using previous dict
    """
    def CreatePredictMatrix(self, path = ""):
        if (not self.trained):
            print "train ClassifierMatrix before predict"
            return False

        #get input path
        inputPath = path
        if (inputPath == ""):
            inputPath = self.curNode.GetChild("test_input")

        f = open(inputPath, "r")
        rows = [0]
        cols = []
        vals = []
        y = []
        for line in f:
            vec = line.split("\t")
            line = vec[0]
            y.append(int(vec[1]))

            #split sentence
            wordList = self.segmenter.Split(line.decode("utf-8"))

            #fill partCols, and create csr
            partCols = []
            termFreqs = {}
            curWordCount = 0
            for word in wordList:
                curWordCount += 1
                if (PyMining.termToId.has_key(word)):
                    termId = PyMining.termToId[word]
                    partCols.append(termId)
                    if (not termFreqs.has_key(termId)):
                        termFreqs[termId] = 1
                    else:
                        termFreqs[termId] += 1

            partCols = set(partCols)
            partCols = list(partCols)
            partCols.sort()
            for col in partCols:
                cols.append(col)
                vals.append(termFreqs[col])
            rows.append(rows[len(rows) - 1] + \
                    len(partCols))

        #close file
        f.close()
        return [Matrix(rows, cols, vals), y]

if __name__ == "__main__":
    config = Configuration.FromFile("conf/test.xml")
    matCreater = ClassifierMatrix(config, "__matrix__")
    [trainMat, ty] = matCreater.CreateTrainMatrix("data/tuangou_titles3.txt")
    [predictMat, py] = matCreater.CreatePredictMatrix("data/tuangou_titles3.txt")
    print py
    print predictMat.rows
    print predictMat.cols
    print predictMat.vals
