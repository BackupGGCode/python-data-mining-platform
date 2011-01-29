if __name__ == "__main__":
    segmenter = Segmenter("test.conf")

    [trainX, trainY] = MatrixCreater.CreateTrainMatrix("trainData", segmenter)
    chiSquareFilter = FeatureSelecter.CreateChiSquareFilter(trainx, trainy, 0.5)
    [trainX, trainY] = chiSquareFilter.Filt(trainX, trainY)
    nbModel = NaiveBayes()
    nbModel.Train(trainX, trainY, args...)

    [testX, testY] = MatrixCreater.CreateTestMatrix("testData", segmenter)
    [testX, testY] = chiSquareFilter.Filt(testX, testY)
    [predictY, precision] = nb.Predict(testX, testY)
    #or
    [predictY] = nb.Predict[testX, testY]
    print precision
