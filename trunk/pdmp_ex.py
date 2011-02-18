if __name__ == "__main__":
    """
    train
    """
    #init dm platfrom, include segmenter..
    config = Configuration.FromFile("test.conf")

    PyMining.Init(config, "global")

    matCreater = ClassifierMatrix(config, "mat_creater")
    [trainx, trainy] = matCreater.CreateTrainMatrix("train.txt")
    #or using matCreater.CreateTrainMatrix(), train corpus will read from config

    chiFilter = ChiSquareFilter(config, "filter")
    [trainx, trainy] = chiFilter.Create(trainx, trainy, .95, "avg")
    #or using chiFilter.Create(trainx, trainy) get default setting in config

    nbModel = NaiveBayes(config, "naive_bayes")
    nbModel.Train(trainx, trainy)

    """
    test
    """
    # config = Configuration("test.conf")

    # PyMining.Init(config, "global", True), True means load from previos file

    # matCreater = ClassifierMatrix(config, "mat_creater", True)
    [testx, testy] = matCreater.CreateTestMatrix(config, "mat_creater")

    #chiFilter = ChiSquareFilter(config, "filter", True)
    [testx, testy] = chiFilter.Filter(testx, testy)

    #nbModel = NaiveBayes(config, "naive_bayes", True)
    [predicty, precision] = nbModel.Predict(testx, testy)
    print precision
