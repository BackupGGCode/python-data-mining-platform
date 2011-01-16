import Matrix
import math

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.featureSet = set()
        self.isLeaf = False
        self.target = -1
        self.variable = -1
        self.leftChild = None
        self.rightChild = None
        for i in range(0, len(self.x.cols)):
            self.featureSet.add(cols[i])

    def Learn():
        #check is split enough(all cate in current node is same)
        tmp = self.y[0]
        isSame = True
        for i in range(1, len(self.y)):
            if tmp != y[i]:
                isSame = False
                break

        #if is same, set current node to leaf node
        if isSame:
            self.isLeaf = True
            self.target = tmp
            return

        #find max-cate num
        maxCate = -1
        for i in range(0, len(y)):
            if (y[i] > maxCate):
                maxCate = y[i]
        
        #else, calculate information-gain(IG(Y|X))
        bestGain = -1000000000
        bestSplit = -1
        for feat in self.featureSet:  
            #get how much cate in current y
            yZeros = [] #when x = 0, counts of y's value
            yOnes = []  #when x = 1, counts of y's value
            xZero = 0   #number of sample[feat] == 0
            xOne = 0    #number of sample[feat] == 1
            for i in range(0, maxCate + 1):
                yZeros.append(0)
                yOnes.append(0)

            #IG(Y|X) = H(Y) - H(Y|X), x is current feature
            #H(Y) = -sigma pj*log(pj,2)
            #          j
            #H(X) = H(Y|x = 0)P(x = 0) + H(Y|x = 1)P(x = 1)
            curGain = 0
            for sample in range(0, len(x.rows) -1):
                value = x.find(sample, feat)
                if (value == 0):
                   yZeros[y[sample]] += 1
                   xZero += 1
                else:
                   yOnes[y[sample]] += 1
                   xOne += 1

            #using yZeros and yOnes Get IG(Y|X)
            #calculate H(Y|x = 0)
            zeroGain = 0
            for i in range(0, maxCate + 1):
                if (yZeros[i] > 0):
                    p = yZero[i] * 1.00 / xZero
                    zeroGain += -1 * p * log(p, 2)
            #calculate H(Y|x = 0) * p(x = 0)
            zeroGain *= xZero * 1.00 / (xZero + xOne)
            #calculate H(Y|x = 1)
            oneGain = 0
            for i in range(0, maxCate + 1):
                if (yOnes[i] > 0):
                    p = yOnes[i] * 1.00 / xOne
                    oneGain += -1 * p * log(p, 2)
            #calculate H(Y|x = 1) * p(x = 1)
            oneGain *= xOne * 1.00 / (xZero + xOne)
            
            if (zeroGain + oneGain > bestGain):
                bestGain = zeroGain + oneGain
                bestSplit = feat

        if (bestSplit < 0):
            print "best split < 0"
            return

        #using bestSplit split x,y to left, right child
        leftRows = [0]
        rightRows = [0]
        leftCols = []
        rightCols = []
        leftVals = []
        rightVals = []
        leftY = []
        rightY = []
        for sample in range(0, x.nRow)
            if x.Get(sample, bestSplit):
                rightRows.append(rightRows[len(rightRows) - 1] + \
                x.rows[sample + 1] - x.rows[sample])
                for i in range(x.rows[sample], x.rows[sample + 1]):
                    rightCols.append(x.cols[i])
                    rightVals.append(x.vals[i])
                rightY.append(y[sample])
            else:
                leftRows.append(leftRows[len(leftRows) - 1] + \
                x.rows[sample + 1] - x.rows[sample])
                for i in range(x.rows[sample, x.rows[sample + 1]):
                    leftCols.append(x.cols[i])
                    leftVals.append(x.vals[i])
                leftY.append(y[sample])
        leftMat = Matrix(leftRows, leftCols, leftVals)
        rightMat = Matrix(rightRows, rightCols, rightVals)
        self.leftChild = Node(leftMat, leftY)
        self.rihgtChild = Node(rightMat, rightY)

        #delete current data
        self.x = None
        self.y = []

    def Predict(self, sample):
        if (self.isLeaf):
            return self.target
        else:
            if (sample.Get(0, self.variable)):
                return self.leftChild.Predict(sample)
            else:
                return self.rightChild.Predict(sample)

