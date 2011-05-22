import math
import pickle
import sys

from matrix import Matrix
from classifier_matrix import ClassifierMatrix
from segmenter import Segmenter
from py_mining import PyMining
from configuration import Configuration 
from chisquare_filter import ChiSquareFilter
from twc_naive_bayes import TwcNaiveBayes


if __name__ == "__main__":
    config = Configuration.FromFile("conf/test.xml")
    PyMining.Init(config, "__global__")
    matCreater = ClassifierMatrix(config, "__matrix__")
    [trainx, trainy] = matCreater.CreateTrainMatrix("data/train.txt")
    chiFilter = ChiSquareFilter(config, "__filter__")
    chiFilter.TrainFilter(trainx, trainy)
    nbModel = TwcNaiveBayes(config, "twc_naive_bayes")
    nbModel.Train(trainx, trainy)

    [testx, testy] = matCreater.CreatePredictMatrix("data/test.txt")
    [testx, testy] = chiFilter.MatrixFilter(testx, testy)
    retY = nbModel.TestMatrix(testx, testy)
