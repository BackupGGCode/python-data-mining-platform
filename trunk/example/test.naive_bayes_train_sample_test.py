#encoding=utf8

from matrix import Matrix
from classifier_matrix import ClassifierMatrix
from segmenter import Segmenter
from py_mining import PyMining
from configuration import Configuration
from chisquare_filter import ChiSquareFilter
from naive_bayes import NaiveBayes

if __name__ == "__main__":
    config = Configuration.FromFile("conf/test.xml")
    PyMining.Init(config, "__global__")
    matCreater = ClassifierMatrix(config, "__matrix__")
    [trainx, trainy] = matCreater.CreateTrainMatrix("data/train.txt")
    chiFilter = ChiSquareFilter(config, "__filter__")
    chiFilter.TrainFilter(trainx, trainy)

    nbModel = NaiveBayes(config, "naive_bayes")
    nbModel.Train(trainx, trainy)
    
    inputStr = "仅售28元！原价698元的康迩福韩国美容美体中心的韩国特色美容套餐1份（紫莱花园店、时代奥城店2店通用）：韩国特色面部SPA护理1次+韩国特色面部瘦脸加毛孔净化1次+韩国特色水"
    [cols, vals] = matCreater.CreatePredictSample(inputStr)
    [cols, vals] = chiFilter.SampleFilter(cols, vals)
    probTuple = nbModel.TestSample(cols, vals)
    print probTuple
