if __name__ == "__main__":
    """
    train
    """
    #init dm platfrom, include segmenter..
    config = Configuration.FromFile("test.conf")

    PyMining.Init(config, "__global__")

    matCreater = ClassifierMatrix(config, "__matrix__")
    [trainx, trainy] = matCreater.CreateTrainMatrix("train.txt")
    #or using matCreater.CreateTrainMatrix(), train corpus will read from config

    chiFilter = ChiSquareFilter(config, "__filter__")
    chiFilter.TrainFilter(trainx, trainy)
    #or using chiFilter.Create(trainx, trainy) get default setting in config

    nbModel = NaiveBayes(config, "naive_bayes")
    nbModel.Train(trainx, trainy)

    """
    test
    """
    # config = Configuration.FromFile("test.conf")

    # PyMining.Init(config, "__global__", True), True means load from previos file

    # matCreater = ClassifierMatrix(config, "__matrix__", True)
    [testx, testy] = matCreater.CreateTestMatrix("test.txt")

    #chiFilter = ChiSquareFilter(config, "__filter__", True)
    [testx, testy] = chiFilter.MatrixFilter(testx, testy)

    #nbModel = NaiveBayes(config, "naive_bayes", True)
    [predicty, precision] = nbModel.Predict(testx, testy)
    print precision
