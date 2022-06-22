import numpy as np
import math
import cv2
import os 
import sys

file_path = sys.argv[1]

gridmap = np.fromfile(file_path , dtype=np.float)
gridsize = gridmap[:2].astype(int)
grid = gridmap[2:]
grid = np.reshape(grid, gridsize)

grid = cv2.resize(grid, (500,500), interpolation = cv2.INTER_LINEAR)

cv2.imshow("window", grid)
cv2.waitKey(0)
