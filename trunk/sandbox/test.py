#coding=utf8=
#mmseg
import matrix
def Segment(line, dicts):
    index = 0
    wordList = []
    while index < len(line):
        finded = False
		#for i = 4 -> 2
        for i in range(2, 4, 1) [::-1]:
            if (i + index <= len(line)):
                if (dicts.has_key(line[index : i + index])):
                        wordList.append(line[index : i + index])
                        index += i
                        finded = True
                        break
        if (finded):
            continue
        index += 1
        
    return wordList

#load dict from a specified path
def LoadDict(dictPath):
    f = open(dictPath, "r")
    dicts = {}
    stopwords = {}
    for line in f:
        line = line.decode("utf-8")
        l = line.split()
        dicts[l[1]] = 1            
    f.close()
    return dicts

#process data file
def CreateMatrixFromData(dataPath):
    #define csr row, col, val
    rows = [0]
    cols = []
    vals = []
	#define target num of each sample
	tars = []

	#1. load dict
	srcDict = LoadDict("E:\src-code\python_platform\dict\\baidu_dict.txt")
	
	#2. open data file, create tarDict from samples
    tarDict = {}
    f = open(dataPath, "r")
    uid = 0
    for line in f:
		#line format as: content \t class
		line = line.decode("utf-8")
		vec = line.split("\t")
		tars.append(vec[1])
		
        words = Segment(line.decode("utf-8"), srcDict)
        for word in words:
            if (not tarDict.has_key(word)):
                tarDict[word] = uid
                uid += 1
				
	#3. re-open data file, using tarDict, and create csr
    f.close()
    f = open("e:\src-code\python_platform\data\\tuangou_titles.txt", "r")
    for line in f:
        words = Segment(line.decode("utf-8"), srcDict)
        partCols = []
        for word in words:
            if (tarDict.has_key(word)):
                partCols.append(tarDict[word])
        partCols = set(partCols)
        partCols = list(partCols)
        for col in partCols:
            cols.append(col)
            vals.append(1)
        rows.append(len(partCols))
	return [rows, cols, vals, tars, tarDict]
	
    
if __name__ == "__main__":
    [rows, cols, vals, tars, tarDict] = CreateMatrixFromData("e:\src-code\python_platform\data\\tuangou_titles.txt")
	x = Matrix(rows, cols, vals, len(rows) - 1, len(tarDict))
