import numpy as np


def move(x=0, y=0):
    return np.array([
        [1, 0, x],
        [0, 1, y],
        [0, 0, 1]
    ], dtype=np.int64)
    
VFLIP = np.array([
    [-1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
], dtype=np.int64)

HFLIP = np.array([
    [1, 0, 0],
    [0, -1, 0],
    [0, 0, 1]
], dtype=np.int64)
    
ROTATE = np.array([
    [0, 1, 0],
    [-1, 0, 0],
    [0, 0, 1]
], dtype=np.int64)
    
INVERSE_ROTATE = np.array([
    [0, -1, 0],
    [1, 0, 0],
    [0, 0, 1]
], dtype=np.int64)