from segmenter import Segmenter
from matrix import Matrix
from py_mining import PyMining
from configuration import Configuration

class ClassifierMatrix:
    def __init__(self, config, nodeName):
        self.node = config.GetChild(nodeName)
        self.segmenter = Segmenter(config, "__segmenter__")
        PyMining.Init(config, "__global__")
        
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
        for line in f:
            vec = line.split("\t")
            line = vec[0]
            target = int(vec[1])
            y.append(target)
            wordList = self.segmenter.Split(line.decode("utf-8"))

            #store current row's cols
            partCols = []

            #create dicts and fill partCol
            for word in wordList:
                if (not PyMining.termToId.has_key(word)):
                    PyMining.termToId[word] = uid
                    PyMining.idToTerm[uid] = word
                    uid += 1
                partCols.append(PyMining.termToId[word])
            partCols = set(partCols)
            partCols = list(partCols)
            partCols.sort()

            #fill cols and vals, fill termToDocCount
            for col in partCols:
                cols.append(col)
                #just keep it simple now
                vals.append(1)
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

        #close file
        f.close()

        #write dicts out
        PyMining.WriteDict(PyMining.termToId, "term_to_id")
        PyMining.WriteDict(PyMining.idToTerm, "id_to_term")
        PyMining.WriteDict(PyMining.classToDocCount, "class_to_doc_count")
        PyMining.WriteDict(PyMining.idToDocCount, "id_to_doc_cout")

        return [Matrix(rows, cols, vals), y] 

    """
    create predict matrix using previous dict
    """
    def CreatePredictMatrix(self, path = ""):
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
            for word in wordList:
                if (PyMining.termToId.has_key(word)):
                    partCols.append(PyMining.termToId[word])
            partCols = set(partCols)
            partCols = list(partCols)
            partCols.sort()
            for col in partCols:
                cols.append(col)
                vals.append(1)
            rows.append(rows[len(rows) - 1] + \
                    len(partCols))

        #close file
        f.close()
        return [Matrix(rows, cols, vals), y]

if __name__ == "__main__":
    config = Configuration.FromFile("conf/test.xml")
    matCreater = ClassifierMatrix(config, "__matrix__")
    [trainMat, ty] = matCreater.CreateTrainMatrix("data/tuangou_titles3.txt")
    [predictMat, py] = matCreater.CreatePredictMatrix("data/tuangou_title3.txt")
