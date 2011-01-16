import random

class Tripple:
    def __init__(self, row, col, val):
        self.row = row
        self.col = col
        self.val = val
    
    def Transpose(self):
        tmp = self.row
        self.row = self.col
        self.col = tmp
        return self
        
def TrippleCmp(t1, t2):
    if (t1.row < t2.row):
        return True
    elif (t1.row > t2.row):
        return False
    else:
        return t1.col < t2.col

class Matrix:
    #init a matrix, using csr, and dimensions
    def __init__(self, rows, cols, vals):
        self.rows = rows
        self.cols = cols
        self.vals = vals
        self.nRow = len(rows) - 1
        maxCol = -1
        for col in cols:
            if (col > maxCol):
                maxCol = col
        self.nCol = maxCol + 1

    #get element @(x,y), if no element, return 0, if range error, return -1
    def Get(self, x, y):
        if (x <= 0) or (x >= self.nRow):
            return -1
        index = bisect.bisect_left(self.cols, y, self.rows[x], self.rows[x + 1])
        if (self.cols[index] == y):
            return 1
        else:
            return 0
    
    def Transpose(self):
        #make transposed-tripple from csr
        triList = []
        for r in range(0, len(self.rows) - 1):
            for c in range(self.rows[r], self.rows[r + 1]):
                t = Tripple(r, self.cols[c], self.vals[c])
                t.Transpose()
                triList.append(t)
        
        #sort tripple
        for t in triList:
            print t.row, " ", t.col, " ", t.val
        print "====="
        sorted(triList, cmp = TrippleCmp)
        for t in triList:
            print t.row, " ", t.col, " ", t.val
        
        #make tripple back to csr
        newRows = []
        newCols = []
        newVals = []
        lastRow = -1
        for i in range(0, len(triList)):
            #add a new row
            if triList[i].row != lastRow:
                newRows.append(i)
                lastRow = triList[i].row
            #add a new col and val
            newCols.append(triList[i].col)
            newVals.append(triList[i].val)
        newRows.append(len(triList))
        return Matrix(newRows, newCols, newVals)

    @staticmethod
    def BaggingFromMatrix(mat, m):
        rows = [0]
        cols = []
        vals = []
        maxCol = -1
        for i in range(0, m):
            ratio = random.random()
            index = int(ratio * mat.nRow)
            print "index:", index
            rows.append(rows[len(rows) - 1] + (mat.rows[index + 1] - mat.rows[index]))
            for j in range(mat.rows[index], mat.rows[index + 1]):
                cols.append(mat.cols[j])
                if (j > maxCol):
                    maxCol = j
                vals.append(mat.vals[j])
        newMat = Matrix(rows, cols, vals, m, maxCol + 1)
        return newMat.Transpose

if __name__ == "__main__":
    rows = [0, 3, 4, 5, 6]
    cols = [0, 1, 2, 3, 4, 4]
    vals = [1, 1, 1, 1, 1, 1]
    mat = Matrix(rows, cols, vals, 4, 5)
    tMat = mat.Transpose()
    #print tMat.rows
    #print tMat.cols
    #print tMat.vals

    sample = Matrix.BaggingFromMatrix(mat, 2)
    print sample.rows
    print sample.cols
    print sample.vals

    sample = Matrix.BaggingFromMatrix(mat, 2)
    print sample.rows
    print sample.cols
    print sample.vals
