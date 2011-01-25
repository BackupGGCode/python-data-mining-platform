#coding=utf8=
#mmseg

from xml.dom import minidom

class Segmenter:
    def __init__(self, confPath):
        domTree = minidom.parse(confPath)
        stopWordPathNode = domTree.getElementsByTagName("stop_word")
        mainDictPathNode = domTree.getElementsByTagName("main_dict")
        self.stopWordDict = stopWordPathNode[0].firstChild.data
        self.mainDict = mainDictPathNode[0].firstChild.data

    def Split(self, line):
        index = 0
        wordList = []
        while index < len(line):
            finded = False
            for i in range(2, 4, 1) [::-1]:
                if (i + index <= len(line)):
                    curWord = line[index : i + index]
                    if (self.mainDict.has_key(curWord) and
                       (not (self.stopWirdDict.has_key(curWord))):
                        wordList.append(line[index : i + 
                                index])
                        index += i
                        finded = True
                        break
             if finded:
                continue
             index += 1
         return wordList

    def LoadDict(self, path):
        f = open(path, "r")
        dicts = {}
        for line in f:
            line = line.decode("utf-8")
            dicts[line] = 1
        f.close()
        return dicts
