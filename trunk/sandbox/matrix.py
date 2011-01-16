class Tripple:
	def __init__(row, col, val):
		self.row = row
		self.col = col
		self.val = val
	
	def Transpose(self):
		tmp = self.row
		self.row = self.col
		self.col = tmp
		return self
		
def TrippleCmp(t1, t2):
	if (t1.row < t2.row):
		return True
	elif (t1.row > t2.row):
		return false
	else:
		return t1.col < t2.col

class Matrix:
	#init a matrix, using csr, and dimensions
	def __init__(self, rows, cols, vals, nRow, nCol):
		self.rows = rows
		self.cols = cols
		self.vals = vals
		self.nRow = nRow
		self.nCol = nCol
	
	def Transpose(self):
		#make transposed-tripple from csr
		triList = []
		for r in range(0, len(rows) - 1):
			for c in range(rows[r], rows[r + 1]):
				t = Tripple(r, cols[c], 1))
				t.Transpose()
				triList.append(t)
		
		#sort tripple
		sorted(triList, cmp = TrippleCmp)
		
		#make tripple back to csr
		newRows = []
		newCols = []
		newVals = []
		lastRow = -1
		for i in range(0, len(triList)):
			#add a new row
			if triList[i].row != lastRow:
				newRows.append(triList[i].row)
				lastRow = triList[i].row
			
			#add a new col and val
			newCols.append(triList[i].col)
			newVals.append(triList[i].val)
		
		return Matrix(newRows, newCols, newVals, nCol, nRow)
		
if __name__ == "__main__":
    rows = [0, 3, 4, 5, 6]
	cols = [0, 1, 2, 3, 4, 5]
	vals = [1, 1, 1, 1, 1, 1]
	mat = Matrix(rows, cols, vals, 4, 5)
	tMat = mat.Transpose()
	print tMat.rows
	print tMat.cols
	print tMat.vals