if __name__ == "__main__":
    segmenter = Segmenter("test.conf")
    [trainX, trainY] = MatrixCreater.CreateTrainMatrix("trainData", segmenter)
    chiFilter = ChiSquareFilter()
    chiFilter.Create(trainX, trainY, 0.8)
    nbModel = NaiveBayes()
    nbModel.Train(trainX, trainY, args...)

    [testX, testY] = MatrixCreater.CreatePredictMatrix("testData", segmenter)
    [testX, testY] = chiFilter.Filter(testX, testY)
    [predictY, precision] = nbModel.Predict(testX, testY)
    #or
    [predictY] = nbModel.Predict[testX, testY]
    print precision
