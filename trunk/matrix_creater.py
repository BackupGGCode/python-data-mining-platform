from xml.dom import minidom
from segmenter import Segmenter
from matrix import Matrix
from dm_material import DmMaterial

class MatrixCreater:
    """
    create train matrix:
        fill dict in DmMaterial, record:
        1)termToId
        2)idToTerm
        3)termToDocCount
        4)classToDocCount
        and save mat-x using csr, save mat-y using list
    """
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
            target = int(vec[1])
            y.append(target)
            wordList = segmenter.Split(line.decode("utf-8"))

            #store current row's cols
            partCols = []

            #create dicts and fill partCol
            for word in wordList:
                if (not DmMaterial.termToId.has_key(word)):
                    DmMaterial.termToId[word] = uid
                    DmMaterial.idToTerm[uid] = word
                    uid += 1
                partCols.append(DmMaterial.termToId[word])
            partCols = set(partCols)
            partCols = list(partCols)
            partCols.sort()

            #fill cols and vals, fill termToDocCount
            for col in partCols:
                cols.append(col)
                #just keep it simple now
                vals.append(1)
                #fill idToDocCount
                if (not DmMaterial.idToDocCount.has_key(col)):
                    DmMaterial.idToDocCount[col] = 1
                else:
                    DmMaterial.idToDocCount[col] += 1

            #fill rows
            rows.append(rows[len(rows) - 1] + \
                len(partCols))

            #fill classToDocCount
            if (not DmMaterial.classToDocCount.has_key(target)):
                DmMaterial.classToDocCount[target] = 1
            else:
                DmMaterial.classToDocCount[target] += 1

        #close file
        f.close()

        return [Matrix(rows, cols, vals), y] 

    """
    create predict matrix using previous dict
    """
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

            #split sentence
            wordList = segmenter.Split(line.decode("utf-8"))

            #fill partCols, and create csr
            partCols = []
            for word in wordList:
                if (DmMaterial.termToId.has_key(word)):
                    partCols.append(DmMaterial.termToId[word])
            partCols = set(partCols)
            partCols = list(partCols)
            for col in partCols:
                cols.append(col)
                vals.append(1)
            rows.append(rows[len(rows) - 1] + \
                    len(partCols))

        #close file
        f.close()
        return [Matrix(rows, cols, vals), y]

if __name__ == "__main__":
    segmenter = Segmenter("test.conf")
    [trainMat, ty] = MatrixCreater.CreateTrainMatrix("data/tuangou_titles3.txt", segmenter)
    [predictMat, py] = MatrixCreater.CreatePredictMatrix("data/tuangou_title3.txt", segmenter)
