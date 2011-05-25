import sys, os
sys.path.append(os.path.join(os.getcwd(), '../'))

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook

#import scipy comp
from scipy import *

#import pymining module
from pymining.math.pca import Pca
from pymining.math.matrix import Matrix
from pymining.math.text2matrix import Text2Matrix
from pymining.common.global_info import GlobalInfo
from pymining.common.configuration import Configuration

if __name__ == "__main__":
    #get pca
    config = Configuration.FromFile("conf/test.xml")
    GlobalInfo.Init(config, "__global__", False)
    txt2mat = Text2Matrix(config, "__matrix__", False)
    [trainx, trainy] = txt2mat.CreateTrainMatrix("data/train.txt")

    pca = Pca()
    pca.TrainPrinComp(trainx, 2, True, False)
    prinCompX = pca.GetPrinComp(trainx, "col")

    #set colors
    colors = []
    for y in trainy:
        if (y == 0):
            colors.append(0.2)
        else:
            colors.append(0.8)

    #draw picture
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(delta1[:0], delta1[:1], c=colors, alpha=0.75)
    plt.show()
