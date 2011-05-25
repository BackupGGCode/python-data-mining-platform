import scipy
import numpy
import scipy.sparse.linalg

#import pymining module
from matrix import *
from scipy_interface import *

class Pca:
    """
    this function get principal component of a given matrix
    @x is the input matrix
    @k is get top-k dimension of pc
    @rowSpace = True, is get U*S
    @colSpace = True, is get S*V'
    @return:
        if rowSpace = True and colSpace = True, return (U*S, S*V')
        if rowSpace = True and colSpace = False, return U*S
        if rowSpace = False and colSpace = True, return S*V'
    """
    @staticmethod
    def GetPrinComp(x, k, colSpace = True, rowSpace = False):
        if (not colSpace) and (not rowSpace):
            print "colSpace and rowSpace both == False, what you want to do?"
            raise

        #do incompelate svd
        csrMat = ScipyInterface.MatrixToCsr(x)

        #get u,s,v'
        (u,s,vt) = scipy.sparse.linalg.svds(csrMat, k)
        s = numpy.diag(s)

        if (colSpace and rowSpace):
            return (numpy.dot(u, s), numpy.dot(s, vt).transpose())

        if (colSpace):
            return numpy.dot(s, vt).transpose()
        
        elif (rowSpace):
            return numpy.dot(u,s) 
