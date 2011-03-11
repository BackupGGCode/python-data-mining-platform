from matrix import Matrix
from classifier_matrix import ClassifierMatrix
from segmenter import Segmenter
from py_mining import PyMining
from configuration import Configuration

class ChiSquareFilter:
    def __init__(self, config, nodeName, loadFromFile = False):
        self.curNode = config.GetChild(nodeName)
        self.rate = float(self.curNode.GetChild("rate").GetValue())
        self.method = self.curNode.GetChild("method").GetValue()
        self.logPath = self.curNode.GetChild("log_path").GetValue()
        self.modelPath = self.curNode.GetChild("model_path").GetValue()
        self.blackList = {}
        self.trained = loadFromFile
        if (loadFromFile):
            f = open(self.modelPath, "r")
            for line in f:
                self.blackList[int(line)] = 1

    def SampleFilter(self, cols, vals):
        if (not self.trained):
            print "train filter before test"
            return False

        #check parameter
        if (len(cols) <> len(vals)):
            print "length of cols should equals length of vals"
            return False

        #filter sample
        newCols = []
        newVals = []
        for c in range(0, len(cols)):
            if not self.blackList.has_key(cols[c]):
                newCols.append(cols[c])
                newVals.append(vals[c])

        return [cols, vals]
    """
    filter given x,y by blackList
    x's row should == y's row
    @return newx, newy filtered
    """
    def MatrixFilter(self, x, y):
        if (not self.trained):
            print "train filter before test"
            return False

        #check parameter
        if (x.nRow <> len(y)):
            print "ERROR!x.nRow should == len(y)"
            return False

        #stores new rows, cols, and vals
        newRows = [0]
        newCols = []
        newVals = []

        for r in range(x.nRow):
            curRowLen = 0

            #debug
            #print "===new doc==="

            for c in range(x.rows[r], x.rows[r + 1]):
                if not self.blackList.has_key(x.cols[c]):
                    newCols.append(x.cols[c])
                    newVals.append(x.vals[c])
                    curRowLen += 1

                    #debug
                    #print PyMining.idToTerm[x.cols[c]].encode("utf-8")

            newRows.append(newRows[len(newRows) - 1] + curRowLen)
        return [Matrix(newRows, newCols, newVals), y]

    """
    create a blackList by given x,y
    @rate is a percentage of selected feature
    using next formulation:
    X^2(t, c) =   N * (AD - CB)^2
                ____________________
                (A+C)(B+D)(A+B)(C+D)
    A,B,C,D is doc-count
    A:     belong to c,     include t
    B: Not belong to c,     include t
    C:     belong to c, Not include t
    D: Not belong to c, Not include t
    
    B = t's doc-count - A
    C = c's doc-count - A
    D = N - A - B - C

    and score of t can be calculated by next 2 formulations:
    X^2(t) = sigma p(ci)X^2(t,ci) (avg)
               i
    X^2(t) = max { X^2(t,c) }     (max)
    @return true if succeed
    """
    def TrainFilter(self, x, y):
        #check parameter
        if not ((self.method == "avg") or (self.method == "max")):
            print "ERROR!method should be avg or max"
            return False

        if (x.nRow <> len(y)):
            print "ERROR!x.nRow should == len(y)"
            return False

        #using y get set of target
        yy = set(y)
        yy = list(yy)
        yy.sort()

        #create a table stores X^2(t, c)
        #create a table stores A(belong to c, and include t
        chiTable = [[0 for i in range(x.nCol)] for j in range(len(yy))]
        aTable = [[0 for i in range(x.nCol)] for j in range(len(yy))]

        #calculate a-table
        for row in range(x.nRow):
            for col in range(x.rows[row], x.rows[row + 1]):
                aTable[y[row]][x.cols[col]] += 1

        #calculate chi-table
        n = x.nRow
        for t in range(x.nCol):
            for cc in range(len(yy)):
                #get a
                a = aTable[cc][t]
                #get b
                b = PyMining.idToDocCount[t] - a
                #get c
                c = PyMining.classToDocCount[cc] - a
                #get d
                d = n - a - b -c
                #get X^2(t, c)
                numberator = float(n) * (a*d - c*b) * (a*d - c*b)
                denominator = float(a+c) * (b+d) * (a+b) * (c+d)
                chiTable[cc][t] = numberator / denominator

        #calculate chi-score of each t
        #chiScore is [score, t's id] ...(n)
        chiScore = [[0 for i in range(2)] for j in range(x.nCol)]
        if (self.method == "avg"):
            #calculate prior prob of each c
            priorC = [0 for i in range(len(yy))]
            for i in range(len(yy)):
                priorC[i] = float(PyMining.classToDocCount[i]) / n

            #calculate score of each t
            for t in range(x.nCol):
                chiScore[t][1] = t
                for c in range(len(yy)):
                    chiScore[t][0] += priorC[c] * chiTable[c][t]
        else:
            #calculate score of each t
            for t in range(x.nCol):
                chiScore[t][1] = t
                for c in range(len(yy)):
                    if (chiScore[t][0] < chiTable[c][t]):
                        chiScore[t][0] = chiTable[c][t]

        #sort for chi-score, and make blackList
        chiScore = sorted(chiScore, key = lambda chiType:chiType[0], reverse = True)

        #add un-selected feature-id to blackList
        for i in range(int(self.rate * len(chiScore)), len(chiScore)):
            self.blackList[chiScore[i][1]] = 1

        #output model information
        if (self.modelPath <> ""):
            f = open(self.modelPath, "w")
            for k in self.blackList:
                f.write(str(k) + "\n")
            f.close()

        #output chiSquare info
        if (self.logPath <> ""):
            f = open(self.logPath, "w")
            f.write("chiSquare info:\n")
            f.write("=======selected========\n")
            for i in range(len(chiScore)):
                if (i == int(self.rate * len(chiScore))):
                    f.write("========unselected=======\n")
                term = PyMining.idToTerm[chiScore[i][1]]
                score = chiScore[i][0]
                f.write(term.encode("utf-8") + " " + str(score) + "\n")
            f.close()

        self.trained = True

        return True

if __name__ == "__main__":
    config = Configuration.FromFile("conf/test.xml")
    PyMining.Init(config, "__global__")
    matCreater = ClassifierMatrix(config, "__matrix__")
    [trainx, trainy] = matCreater.CreateTrainMatrix("data/tuangou_titles3.txt")
    chiFilter = ChiSquareFilter(config, "__filter__")
    chiFilter.TrainFilter(trainx, trainy) 
