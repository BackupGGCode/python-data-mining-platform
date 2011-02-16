#coding=utf8=
#mmseg

from configuration import Configuration

class Segmenter:
    def __init__(self, config, nodeName):
        curNode = config.GetChild(nodeName)
        self.minIdf = float(curNode.GetChild("min_idf").GetValue())
        self.maxIdf = float(curNode.GetChild("max_idf").GetValue())
        self.stopWordDict = self.LoadStopWordDict(curNode.GetChild("stop_word").GetValue())
        self.mainDict = self.LoadMainDict(curNode.GetChild("main_dict").GetValue())

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
    
    cfg = Configuration.FromFile("conf/test.xml")
    segmenter = Segmenter(cfg, "segmenter")
    f = open("data/tuangou_titles3.txt")
    for line in f:
        wordList = segmenter.Split(line.decode("utf-8"))
        for word in wordList:
            print word.encode("utf-8")
