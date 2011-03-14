import math
import pickle
import sys

from matrix import Matrix
from classifier_matrix import ClassifierMatrix
from segmenter import Segmenter
from py_mining import PyMining
from configuration import Configuration 

class TwcNaiveBayes:
    def __init__(self, config, nodeName, loadFromFile = False):
        #store weight from term->class
        weights = []

        self.trained = loadFromFile
        self.curNode = config.GetChild(nodeName)
        self.modelPath = self.curNode.GetChild("model_path").GetValue()
        self.logPath = self.curNode.GetChild("log_path").GetValue()

        if (loadFromFile):
            f = open(self.modelPath, "r")
            modelStr = pickle.load(f)
            [self.weights, self.yy] = pickle.loads(modelStr)
            f.close()

    def Train(self, x, y):
        #check parameters
        if (x.nRow <> len(y)):
            print "Error!, x.nRow should equals len(y)"
            return False
        
        """
        calculate d(i(term),j(doc))
        1. d(i,j) = log(d(i,j) + 1)
        2. d(i,j) = d(i,j) * idf(i)
        3. d(i,j) = d(i,j) / sqrt(sigma(d(k,j)^2))
                            k belong current sample
        """
        for r in range(len(x.rows) - 1):
            sampleSum = 0.0
            for c in range(x.rows[r], x.rows[r + 1]):
                termId = x.cols[c]
                x.vals[c] = math.log(x.vals[c] + 1)
                x.vals[c] = x.vals[c] * PyMining.idToIdf[termId]
                sampleSum += x.vals[c] * x.vals[c]

            #normalize it
            sampleSum = math.sqrt(sampleSum)
            for c in range(x.rows[r], x.rows[r + 1]):
                x.vals[c] = float(x.vals[c]) / sampleSum
        
        """
        calculate weights
        1. theta(c, i) = sigma d(i,j) + alpha(i)
                        j(y(j) not c
                        ________________________________
                         sigma      sigma d(k, j) + sum(alpha)
                        j(y(j) != c)  k
                        
                        (alpha(i) = 1)
                        (sum(alpha(i)) = len(y)
        2. w(c, i) = log(theta(c,i))
        3. w(c, i) = w(c, i) / sigma(w(c, i))
                                 i 
        """
        self.yy = set(y)
        self.yy = list(self.yy)
        self.yy.sort()
        #init weights:
        self.weights = [[0 for j in range(x.nCol)] for i in range(len(self.yy))]
        weightsSum = [0 for i in range(len(self.yy))]
        #calculate theta(c,i) = sigma d(i,j) + 1
        #                      y(j)<>c
        for classId in range(len(self.yy)):
            for r in range(len(x.rows) - 1):
                for c in range(x.rows[r], x.rows[r + 1]):
                    if (y[r] <> self.yy[classId]):
                        termId = x.cols[c]
                        self.weights[classId][termId] += x.vals[c]
                        weightsSum[classId] += x.vals[c]
        #normalize weights
        classCount = len(self.yy)
        for classId in range(len(self.yy)):
            curClassSum = 0
            for termId in range(x.nCol):
                self.weights[classId][termId] += 1
                self.weights[classId][termId] /= float(weightsSum[classId]) + classCount
                self.weights[classId][termId] = math.log(self.weights[classId][termId])
                curClassSum += self.weights[classId][termId]
            for termId in range(x.nCol):
                self.weights[classId][termId] /= curClassSum

        self.trained = True
        #dump model
        f = open(self.modelPath, "w")
        modelStr = pickle.dumps([self.weights, self.yy], 1)
        pickle.dump(modelStr, f)
        f.close()

        return True

    """
    l(t) = argmin sigma t(i) * w(c,i)
            c       i
           (t(i) is frequency of termI in this sample)
    """
    def __GetBestTarget(self, cols, vals):
        if (len(cols) <> len(vals)):
            print "Error!, len of cols should == len of vals"
            return -1

        #get min likelihood
        #minL = sys.maxint
        retList = []

        maxL = -1
        bestClass = 0
        sumProb = 0
        for classIndex in range(len(self.yy)):
            curL = 0
            for c in range(len(cols)):
                termId = cols[c]
                termFreq = vals[c]
                curL += termFreq * self.weights[classIndex][termId]

            retList.append([self.yy[classIndex], curL]) 
            sumProb += curL

        for i in range(len(retList)):
            retList[i][1] /= (sumProb + 1e-10)
            retList[i] = tuple(retList[i])
       
        return tuple(retList)

    """
    get result of a single-line-sample
    """
    def TestSample(self, cols, vals):
        #check parameter
        if (not self.trained):
            print "Error!, not trained!"
            return ()

        ret = self.__GetBestTarget(cols, vals)
        return ret

    """
    get result of a multi-line-sample
    """
    def TestMatrix(self, x, y = None):
        retY = []
        correct = 0

        for r in range(x.nRow):
            ret = self.__GetBestTarget(x.cols[x.rows[r]:x.rows[r + 1]], x.vals[x.rows[r]:x.rows[r + 1]])
            retY.append(ret)
            if (y <> None):
                bestL = -1
                bestTarget = 0
                for tup in ret:
                    if (tup[1] > bestL):
                        bestL = tup[1]
                        bestTarget = tup[0]
                if (bestTarget == y[r]):
                    correct += 1

        if (y <> None):
            print "precision : ", float(correct) / x.nRow

        return retY

if __name__ == "__main__":
    config = Configuration.FromFile("conf/test.xml")
    PyMining.Init(config, "__global__")
    matCreater = ClassifierMatrix(config, "__matrix__")
    [trainx, trainy] = matCreater.CreateTrainMatrix("data/train.txt")
    nbModel = TwcNaiveBayes(config, "twc_naive_bayes")
    nbModel.Train(trainx, trainy)

    [testx, testy] = matCreater.CreatePredictMatrix("data/test.txt")
    retY = nbModel.TestMatrix(testx, testy)
