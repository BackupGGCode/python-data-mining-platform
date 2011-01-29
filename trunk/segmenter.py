#coding=utf8=
#mmseg

from xml.dom import minidom

class Segmenter:
    def __init__(self, confPath):
        domTree = minidom.parse(confPath)
        stopWordPathNode = domTree.getElementsByTagName("stop_word")
        mainDictPathNode = domTree.getElementsByTagName("main_dict")
        minIdfNode = domTree.getElementsByTagName("min_idf")
        maxIdfNode = domTree.getElementsByTagName("max_idf")
        self.minIdf = float(minIdfNode[0].firstChild.data)
        self.maxIdf = float(maxIdfNode[0].firstChild.data)
        self.stopWordDict = self.LoadStopWordDict(stopWordPathNode[0].firstChild.data)
        self.mainDict = self.LoadMainDict(mainDictPathNode[0].firstChild.data)

    def Split(self, line):
        line = line.lower()
        index = 0
        wordList = []
        while index < len(line):
            finded = False
            for i in range(1, 5, 1) [::-1]:
                if (i + index <= len(line)):
                    curWord = line[index : i + index]
                    if (self.mainDict.has_key(curWord)) and (not (self.stopWordDict.has_key(curWord))):
                        wordList.append(line[index : i + index])
                        index += i
                        #index += 1
                        finded = True
                        break
            if (finded):
                continue
            index += 1
        return wordList

    def LoadStopWordDict(self, path):
        f = open(path, "r")
        dicts = {}
        for line in f:
            line = line.decode("utf-8")
            dicts[line] = 1
        f.close()
        return dicts

    def LoadMainDict(self, path):
        f = open(path, "r")
        dicts = {}
        for line in f:
            line = line.decode("utf-8")
            vec = line.split("\t")
            vec[1] = float(vec[1])
            if (vec[1] > self.minIdf) and (vec[1] < self.maxIdf):
                dicts[vec[0]] = vec[1]
        f.close()
        return dicts

if __name__ == "__main__":
    segmenter = Segmenter("test.conf")
    f = open("data/tuangou_titles3.txt")
    for line in f:
        wordList = segmenter.Split(line.decode("utf-8"))
        print wordList
