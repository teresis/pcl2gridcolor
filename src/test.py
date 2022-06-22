import numpy as np
import math
import cv2
import os 
HEADER_LINE_NUM = 11
THRESHOLD1 = 4
THRESHOLD2 = 16
SCALE = 5
file_path = "/mnt/d/data/pcd/voxelized.pcd"
file_path = "/mnt/d/data/pcd/raw2vox"
file_list = os.listdir(file_path)

for f in file_list:
	fp = open(file_path + "/" + f, "r")
	pointNum = 0
	for i in range(HEADER_LINE_NUM):
		line = fp.readline()
		tokens = line.split()
		if(tokens[0] == 'POINTS'):
			pointNum = int(tokens[1])

	points = np.zeros((pointNum,3))
	for i in range(pointNum):
		line = fp.readline()
		tokens = line.split()
		points[i] = list(map(float, tokens))

#p75, p25 = np.percentile(points[:,0], [99.9, 0.1])
#points = points[points[:, 0] < p75]
#points = points[points[:, 0] > p25]
	x_max = np.max(points[:,0])
	x_min = math.floor(np.min(points[:,0]))

#p75, p25 = np.percentile(points[:,2], [99.9, 0.1])
#points = points[points[:, 2] < p75]
#points = points[points[:, 2] > p25]
	z_max = np.max(points[:,2])
	z_min = math.floor(np.min(points[:,2]))
	print(x_max,z_max)
	print(x_min,z_min)
	print(points.shape[0])
	pointNum = points.shape[0]
	grid = np.zeros((150,150))
	for i in range(pointNum):
		x,y,z= points[i].astype(int)
		x=int(x//SCALE + abs(x_min)//SCALE)
		z=int(z//SCALE + abs(z_min)//SCALE)
 		grid[z][x]+=1

	for r in range(len(grid)):
		 for c in range(len(grid[r])):
			 if grid[r][c] < THRESHOLD1:
				 grid[r][c] = 0
			 elif grid[r][c] < THRESHOLD2:
				 grid[r][c] = 0.5
			 else:
				 grid[r][c] = 1

	grid = cv2.resize(grid, (500,500), interpolation = cv2.INTER_LINEAR)
	grid.tofile(f+".bin")
	cv2.imshow("window", grid)
	cv2.waitKey(0)
	cv2.imwrite(f+".jpg",grid)
