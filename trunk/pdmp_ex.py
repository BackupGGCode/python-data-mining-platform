if __name__ == "__main__":
    """
    train
    """
    #init dm platfrom, include segmenter..
    config = Configuration("test.conf")

    DmPlatform.Init(config, "global")

    matCreater = MatrixCreater(config, "mat_creater")
    [trainx, trainy] = matCreater.CreateTrainMatrix(config, "source_train")

    chiFilter = ChiSquareFilter(config, "filter")
    [trainx, trainy] = chiFilter.Create(trainx, trainy, .95, "avg")

    nbModel = NaiveBayes(config, "naive_bayes")
    nbModel.Train(trainx, trainy)

    """
    test
    """
    # config = Configuration("test.conf")

    # DmPlatfrom.Init(config, "global", True), True means load from previos file

    # matCreater = MatrixCreater(config, "mat_creater", True)
    [testx, testy] = matCreater.CreateTestMatrix(config, "mat_creater")

    #chiFilter = ChiSquareFilter(config, "filter", True)
    [testx, testy] = chiFilter.Filter(testx, testy)

    #nbModel = NaiveBayes(config, "naive_bayes", True)
    [predicty, precision] = nbModel.Predict(testx, testy)
    print precision

    




