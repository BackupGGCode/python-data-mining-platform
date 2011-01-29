from matrix import Matrix

class ChiSqaureFilter:
    def __init__(self):
        self.blackList = {}

    """
    filter given x,y by blackList
    x's row should == y's row
    @return newx, newy filtered
    """
    def Filter(x, y):
        return [newx, newy]

    """
    create a blackList by given x,y
    @rate is a percentage of selected feature
    using next formulation:
    X^2(t, c) =   N * (AD - CD)^2
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
    def Create(x, y, rate, method = "avg"):
        #check parameter
        if not ((method == "avg") or (method == "max")):
            print "ERROR!method should be avg or max"
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
                aTable[x.cols[col]][y[row]] += 1

        #calculate chi-table
        n = x.nRow
        for t in range(x.nCol):
            for c in range(len(yy)):
                #get a
                a = aTable[t][c]
                #get b
                b = DmMaterial.idToDocCount[t] - a
                #get c
                c = DmMaterial.classToDocCount[c] - a
                #get d
                d = n - a - b -c
                #get X^2(t, c)
                numberator = float(n) * (a*d - c*d) * (a*d - c*d)
                denominator = float(a+c) * (b+d) * (a+b) * (c+d)
                chiTable[t][c] = numberator / demoninator

        #calculate chi-score of each t
        #chiScore is [score, t's id] ...(n)
        chiScore = [[0 for i in range(2)] for j in range(x.nCol)]
        if (method == "avg"):
            #calculate prior prob of each c
            priorC = [0 for i in range(len(yy))]
            for i in range(len(yy)):
                priorC[i] = float(DmMaterial.classToDocCount[i]) / n

            #calculate score of each t
            for t in range(x.nCol):
                chiScore[t][1] = t
                for c in range(len(yy)):
                    chiScore[t][0] += priorC[c] * chiTable[t][c]
        else if (method = "max"):
            #calculate score of each t
            for t in range(x.nCol):
                chiScore[t][1] = t
                for c in range(len(yy)):
                    if (chiScore[t][0] > chiTable[t][c]):
                        chiScore[t][0] = chiTable[t][c]

        #sort for chi-score, and make blackList
        sorted(chiScore, key = lambda chiType : chiType[0])

        #add un-selected feature-id to blackList
        for i in range(int(rate * len(chiScore)), len(chiScore)):
            self.blackList[chiScore[i][1]] = 1

        #output chiSquare info
        print "=======selected========"
        for i in range(len(chiScore)):
            if (i == int(rate * len(chiScore))):
                print "========unselected======="
            term = DmMaterial.idToTerm[chiScore[i][1]]
            score = chiScore[i][0]
            print term.encode("utf-8"), " ", score

        return True

if __name__ == "__main__":
    segmenter = Segmenter("test.conf")
    [trainX, trainY] = MatrixCreater.CreateTrainMatrix("data/train.txt", segmenter)
    chiFilter = ChiSquareFilter()
    chiFilter.Create(trainX, trainY, 0.8)
   
