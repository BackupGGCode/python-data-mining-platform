from xml.dom import minidom
from segmenter import Segmenter
from matrix import Matrix

class MatrixCreater:
    def __init__(self, confPath):
        domTree = minidom.parse(confPath)
        savePathNode = domTree.getElementsByTagName("save_dict_path")
        self.savePath = savePathNode[0].firstChild.data
        self.saveDict = {}
        self.termCount = {}

    def CreateTrainMatrix(self, inputPath, segmenter):
        f = open(inputPath, "r")
        uid = 0
        rows = [0]
        cols = []
        vals = []
        y = []
        for line in f:
            vec = line.split("\t")
            line = vec[0]
            y.append(int(vec[1]))
            wordList = segmenter.Split(line.decode("utf-8"))
            partCols = []
            for word in wordList:
                if (not self.saveDict.has_key(word)):
                    self.saveDict[word] = uid
                    uid += 1
                    self.termCount[word] = 1
                else:
                    self.termCount[word] += 1
                partCols.append(self.saveDict[word])
            partCols = set(partCols)
            partCols = list(partCols)
            partCols.sort()
            for col in partCols:
                cols.append(col)
                #just keep it simple now
                vals.append(1)
            rows.append(rows[len(rows) - 1] + \
                len(partCols))
        f.close()

        #filter features
        for word in self.termCount:
            if (self.termCount[word] <= 1) or (self.termCount[word] >= len(rows) * 0.7):
                del self.saveDict[word]

        return [Matrix(rows, cols, vals), y] 

    def CreatePredictMatrix(self, inputPath, segmenter):
        f = open(inputPath, "r")
        rows = [0]
        cols = []
        vals = []
        y = []
        for line in f:
            vec = line.split("\t")
            line = vec[0]
            y.append(int(vec[1]))
            wordList = segmenter.Split(line.decode("utf-8"))
            partCols = []
            for word in wordList:
                if (self.saveDict.has_key(word)):
                    partCols.append(self.saveDict[word])
            partCols = set(partCols)
            partCols = list(partCols)
            for col in partCols:
                cols.append(col)
                vals.append(1)
            rows.append(rows[len(rows) - 1] + \
                    len(partCols))
        f.close()
        return [Matrix(rows, cols, vals), y]

if __name__ == "__main__":
    segmenter = Segmenter("test.conf")
    matCreater = MatrixCreator("test.conf")
    [trainMat, ty] = matCreater.CreateTrainMatrix("data/tuangou_titles3.txt", segmenter)
    [predictMat, py] = matCreater.CreatePredictMatrix("data/tuangou_title3.txt", segmenter)
