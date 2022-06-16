import numpy as np
import math
import cv2
import os 
import sys

file_path = sys.argv[1]

grid = np.fromfile(file_path , dtype=np.float)
shape = int(np.sqrt(grid.shape[0]))
print(shape)
print(grid)
grid = np.reshape(grid, (shape, shape))
grid = cv2.resize(grid, (500,500), interpolation = cv2.INTER_LINEAR)

cv2.imshow("window", grid)
cv2.waitKey(0)
