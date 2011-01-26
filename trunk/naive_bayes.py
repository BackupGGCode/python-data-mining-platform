import math

from matrix import Matrix
from matrix_creater import MatrixCreater
from segmenter import Segmenter

class NaiveBayes:
    def __init__(self, path, segmenter):
        self.segmenter = segmenter
        self.matCreater = MatrixCreater(path)

        #store variable(term)'s likelihood to each class
        self.vTable = []
        #store prior of each class
        self.cPrior = []
        #store isTrained by data
        self.trained = False

    def Train(self, trainData):
        [mat, y] = self.matCreater.CreateTrainMatrix(\
                trainData, self.segmenter)
        
        #calculate prior of each class
        #1. init cPrior:
        tmp = set(y)
        tmp = list(tmp)
        tmp.sort()
        self.cPrior = [0 for i in range(tmp[len(tmp) - 1] + 1)]
        for i in y:
            self.cPrior[i] += 1

        #calculate likehood of each term
        #1. init vTable:
        self.vTable = [[0 for i in range(len(self.cPrior))] \
                for j in range(mat.nCol)]
        #2. fill vTable
        for r in range(mat.nRow):
            for i in range(mat.rows[r], mat.rows[r + 1]):
                self.vTable[mat.cols[i]][y[r]] += 1
        
        #normalize vTable and cPrior
        for i in range(mat.nCol):
            for j in range(len(self.cPrior)):
                self.vTable[i][j] /= self.cPrior[j]
        for i in range(len(self.cPrior)):
            self.cPrior[i] /= float(len(y))
        self.trained = True

    def Predict(self, testData):
        if (not self.trained):
            print "not trained!"
            return

        [mat, y] = self.matCreater.CreatePredictMatrix(\
                testData, self.segmenter)

        retY = []
        correct = 0
        for r in range(mat.nRow):
            bestY = -1
            maxP = -1000000000
            for target in range(len(self.cPrior)):
                curP = 0
                curP += math.log(self.cPrior[target])
                for c in range(mat.rows[r], mat.rows[r + 1]):
                    if (self.vTable[mat.cols[c]][target] == 0):
                        curP += math.log(1e-7)
                    else:
                        curP += math.log(self.vTable[mat.cols[c]][target])
                if (curP > maxP):
                    bestY = target
            if (bestY < 0):
                print "best y < 0, error!"
                break
            if (bestY == y[r]):
                correct += 1
            retY.append(bestY)

        return [retY, float(correct) / len(retY)]

if __name__ == "__main__":
    segmenter = Segmenter("test.conf")
    nb = NaiveBayes("test.conf", segmenter)
    nb.Train("data/tuangou_titles3.txt")
    [tarY, precision] = nb.Predict("data/tuangou_titles3.txt")
    print "precision:", precision
