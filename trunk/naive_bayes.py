import math

from matrix import Matrix
from matrix_creater import MatrixCreater
from segmenter import Segmenter
from chisquare_filter import ChiSquareFilter
from dm_material import DmMaterial

class NaiveBayes:
    def __init__(self):
        #store variable(term)'s likelihood to each class
        self.vTable = []
        #store prior of each class
        self.cPrior = []
        #store isTrained by data
        self.trained = False

    def Train(self, x, y):
        #check parameters
        if (x.nRow <> len(y)):
            print "ERROR!, x.nRow should == len(y)"
            return False

        #calculate prior of each class
        #1. init cPrior:
        yy = set(y)
        yy = list(yy)
        yy.sort()
        self.cPrior = [0 for i in range(len(yy))]

        #2. fill cPrior
        for i in y:
            self.cPrior[i] += 1

        #calculate likehood of each term
        #1. init vTable:
        self.vTable = [[0 for i in range(len(self.cPrior))] \
                for j in range(x.nCol)]

        #2. fill vTable
        for r in range(x.nRow):
            for i in range(x.rows[r], x.rows[r + 1]):
                self.vTable[x.cols[i]][y[r]] += 1
        
        #normalize vTable
        for i in range(x.nCol):
            for j in range(len(self.cPrior)):
                self.vTable[i][j] /= float(self.cPrior[j])
        
        #normalize cPrior
        for i in range(len(self.cPrior)):
            self.cPrior[i] /= float(len(y))

        self.trained = True
        return True

    def Predict(self, x, y):
        #check parameter
        if (not self.trained):
            print "Error!, not trained!"
            return False
        
        if (x.nRow != len(y)):
            print "Error! x.nRow should == len(y)"
            return False

        retY = []
        correct = 0

        #predict all doc one by one
        for r in range(x.nRow):
            bestY = -1
            maxP = -1000000000

            #debug
            print "\n ===============new doc================="

            #calculate best p
            for target in range(len(self.cPrior)):
                curP = 0
                curP += math.log(self.cPrior[target])
                
                #debug
                print "<target> : ", target

                for c in range(x.rows[r], x.rows[r + 1]):
                    if (self.vTable[x.cols[c]][target] == 0):
                        curP += math.log(1e-7)
                    else:
                        curP += math.log(self.vTable[x.cols[c]][target])

                    #debug
                    term = DmMaterial.idToTerm[x.cols[c]]
                    prob = math.log(self.vTable[x.cols[c]][target] + 1e-7) 
                    print term.encode("utf-8"), ":", x.cols[c], ":", prob


                if (curP > maxP):
                    bestY = target
                    maxP = curP

                #debug
                print "curP:", curP

            if (bestY < 0):
                print "best y < 0, error!"
                return False
            if (bestY == y[r]):
                correct += 1
            #debug
            else:
                print "predict error!"

            retY.append(bestY)
        
        return [retY, float(correct) / len(retY)]

if __name__ == "__main__":
    segmenter = Segmenter("test.conf")
    [trainX, trainY] = MatrixCreater.CreateTrainMatrix("data/train.txt", segmenter)
    chiFilter = ChiSquareFilter()
    chiFilter.Create(trainX, trainY, .97, "avg")
    nbModel = NaiveBayes()
    nbModel.Train(trainX, trainY)

    [testX, testY] = MatrixCreater.CreatePredictMatrix("data/test.txt", segmenter)
    [testX, testY] = chiFilter.Filter(testX, testY)
    
    """
    print "testX, rows, cols ,vals"
    print testX.rows
    print testY
    print testX.cols
    """

    [predictY, precision] = nbModel.Predict(testX, testY)
    print precision
