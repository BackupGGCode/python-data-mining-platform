if __name__ == "__main__":
    segmenter = Segmenter("test.conf")
    
    nb = NaiveBayes("test.conf", segmenter)
    nb.Train("train.data")
    [predictY, precision] = nb.Predict("test.data")
    print precision
