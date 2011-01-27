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
        #store which term(feature-id) is useless
        self.blackList = {}

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
                self.vTable[i][j] /= float(self.cPrior[j])
            #test if need add to blackList
            aboveZero = 0
            for j in range(len(self.cPrior)):
                if self.vTable[i][j] > 1e-5:
                    aboveZero += 1
            if (aboveZero >= len(self.cPrior)):
                self.blackList[i] = 1
        #debug - output prob of vTable
        for word in self.matCreater.saveDict:
            print word.encode("utf-8"), " ", self.vTable[self.matCreater.saveDict[word]]

        for i in range(len(self.cPrior)):
            self.cPrior[i] /= float(len(y))
        self.trained = True

        #debug - print blackList:
        print self.blackList

    def Predict(self, testData):
        if (not self.trained):
            print "not trained!"
            return

        [mat, y] = self.matCreater.CreatePredictMatrix(\
                testData, self.segmenter)

        #debug
        f = open(testData, "r")
        lines = []
        for line in f:
            lines.append(line)
        f.close()

        retY = []
        correct = 0
        for r in range(mat.nRow):
            bestY = -1
            maxP = -1000000000
            #debug
            #print lines[r]
            #print y[r]
            for target in range(len(self.cPrior)):
                curP = 0
                curP += math.log(self.cPrior[target])
                for c in range(mat.rows[r], mat.rows[r + 1]):
                    #if (self.blackList.has_key(mat.cols[c])):
                    #    continue
                    if (self.vTable[mat.cols[c]][target] == 0):
                        curP += math.log(1e-7)
                    else:
                        curP += math.log(self.vTable[mat.cols[c]][target])
                #debug, output prob of each document of predict
                #print curP

                if (curP > maxP):
                    bestY = target
                    maxP = curP
            if (bestY < 0):
                print "best y < 0, error!"
                break
            if (bestY == y[r]):
                correct += 1
            #debug
            else:
                print lines[r], " : ", bestY
            retY.append(bestY)
        
        return [retY, float(correct) / len(retY)]

if __name__ == "__main__":
    segmenter = Segmenter("test.conf")
    nb = NaiveBayes("test.conf", segmenter)
    nb.Train("data/train.txt")
    [tarY, precision] = nb.Predict("data/test.txt")
    print "precision:", precision
