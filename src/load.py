import numpy as np
import math
import cv2
import os 

file_path = "../data/"
file_list = os.listdir(file_path)
print(file_list)
for f in file_list:
	print(file_path + f)
	grid = np.fromfile(file_path + f, dtype=np.float)
	grid = np.reshape(grid, (500, 500))
	print(grid.shape)
	print(grid[np.nonzero(grid)])
	cv2.imshow("window", grid)
	cv2.waitKey(0)
