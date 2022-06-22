import numpy as np
import math
import cv2
import os 
import sys

HEADER_LINE_NUM = 11
THRESHOLD1 = 8
THRESHOLD2 = 32
SCALE = 4
OFFSET = 10
file_path = sys.argv[1]

fp = open(file_path, "r")

''' read pcd file'''
print("reading pcd file...")
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

x_max = np.max(points[:,0])
x_min = np.min(points[:,0])
z_max = np.max(points[:,2])
z_min = np.min(points[:,2])

gridsize = (int(z_max//SCALE + abs(x_min)//SCALE + 2*OFFSET), int(x_max//SCALE + abs(x_min)//SCALE + 2*OFFSET))
grid = np.zeros((gridsize))

print("(x max, x min) : ",x_max, x_min)
print("(z max, z min) : ",z_max, z_min)
print("grid size : ",gridsize)

''' generate grid '''
print("generating grid...")
for i in range(points.shape[0]):
	x,y,z= points[i].astype(int)
	x=int(x//SCALE + abs(x_min)//SCALE)
	z=int(z//SCALE + abs(z_min)//SCALE)
	grid[z+OFFSET][x+OFFSET]+=1

for r in range(len(grid)):
	 for c in range(len(grid[r])):
		 if grid[r][c] < THRESHOLD1:
			 grid[r][c] = 0
		 elif grid[r][c] < THRESHOLD2:
			 grid[r][c] = 0.5
		 else:
			 grid[r][c] = 1

grid.tofile(file_path+".bin")

grid = cv2.resize(grid, (500,500), interpolation = cv2.INTER_LINEAR)
cv2.imshow("window", grid)
cv2.waitKey(0)
