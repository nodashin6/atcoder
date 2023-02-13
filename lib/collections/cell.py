class Cell:

    DIRECTIONS = ((0, -1), (0, 1), (-1, 0), (1, 0))
    
    def __init__(self, cells):
        self.cells = cells
        self.H = len(cells)
        self.W = len(cells[0])

    def __getitem__(self, index):
        if type(index) is int:
            return self.cells[index]
        elif hasattr(index, "__iter__"):
            i, j = index[0], index[1]
            return self.cells[i][j]
        raise IndexError
    
    def __setitem__(self, index, value):
        if type(index) is int:
            self[index] = value
            return
        elif hasattr(index, "__iter__"):
            i, j = index[0], index[1]
            self[i][j] = value
            return
        raise IndexError
    
    def isin(self, pos):
        return 0<=pos[0]<self.H and 0<=pos[1]<self.W