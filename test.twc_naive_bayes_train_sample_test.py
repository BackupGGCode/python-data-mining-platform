#encoding=utf-8

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
    nbModel = TwcNaiveBayes(config, "twc_naive_bayes")
    nbModel.Train(trainx, trainy)

    inputStr = "仅售59元！原价108元的花园巴西烤肉自助餐一人次任吃（蛇口店、购物公园店全时段通用），另赠送两张10元现金抵用券！邀请好友返利10元！"
    [cols, vals] = matCreater.CreatePredictSample(inputStr.decode("utf-8"))
    retY = nbModel.TestSample(cols, vals)
    print retY
