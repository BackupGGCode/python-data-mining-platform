from matrix import Matrix
from classifier_matrix import ClassifierMatrix
from segmenter import Segmenter
from py_mining import PyMining
from configuration import Configuration
from chisquare_filter import ChiSquareFilter
from naive_bayes import NaiveBayes

if __name__ == "__main__":
    config = Configuration.FromFile("conf/test.xml")
    PyMining.Init(config, "__global__", True)
    matCreater = ClassifierMatrix(config, "__matrix__", True)
    chiFilter = ChiSquareFilter(config, "__filter__", True)

    nbModel = NaiveBayes(config, "naive_bayes", True)

    [testx, testy] = matCreater.CreatePredictMatrix("data/test.txt")
    [testx, testy] = chiFilter.TestFilter(testx, testy)
    [resultY, precision] = nbModel.Test(testx, testy)
    
    print precision
