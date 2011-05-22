import sys, os
sys.path.append(os.path.join(os.getcwd(), '../'))

from pymining.math.matrix import Matrix
from pymining.math.classifier_matrix import ClassifierMatrix
from pymining.nlp.segmenter import Segmenter
from pymining.common.py_mining import PyMining
from pymining.common.configuration import Configuration
from pymining.preprocessor.chisquare_filter import ChiSquareFilter
from pymining.classifier.naive_bayes import NaiveBayes

if __name__ == "__main__":
    config = Configuration.FromFile("conf/test.xml")
    PyMining.Init(config, "__global__", True)
    matCreater = ClassifierMatrix(config, "__matrix__", True)
    chiFilter = ChiSquareFilter(config, "__filter__", True)

    nbModel = NaiveBayes(config, "naive_bayes", True)

    [testx, testy] = matCreater.CreatePredictMatrix("data/test.txt")
    [testx, testy] = chiFilter.MatrixFilter(testx, testy)
    [resultY, precision] = nbModel.Test(testx, testy)
    
    print precision
