import Matrix
import Node
import math

class RandomForest
    #build a forest consist of nTree trees
    #and each tree have (int)(ratio * nFeatures) variables
    def __init__(self, x, y, nTree, ratio):
        self.nTree = nTree
        self.nFeature = int(x.nCol * ratio)
        self.x = x
        self.y = y

    def Learn(self):
        #get transpose of x
        tX = self.x.Transpose()

        #spawn forest
        self.trees = []
        for i in range(0, self.nTree):
            subX = Matrix.BaggingFromMatrix(tX, self.nFeature)
            node = Node(subX, self.y)
            node.Learn()
            self.trees.append(node)

    def Predict(self, sample):
        results = {}
        for i in range(0, self, nTree):
            result = self.trees[i].Predict(sample)
            if not results.has_key(result):
                results[result] = 0
            else:
                result[self.trees[i].Predict(sample)] += 1

        bestResult = -1
        maxNum = -1
        for result in results:
            if results[result] > maxNum:
                maxNum = results[result]
                bestResult = result

        return bestResult
