import numpy as np
import math
import cv2

HEADER_LINE_NUM = 11
THRESHOLD1 = 32
THRESHOLD2 = 64

with open("../map.pcd", "r") as file:
    pointNum = 0
    for i in range(HEADER_LINE_NUM):
        line = file.readline()
        tokens = line.split()
        if(tokens[0] == 'POINTS'):
            pointNum = int(tokens[1])
    
    points = np.zeros((pointNum,3))
    for i in range(pointNum):
        line = file.readline()
        tokens = line.split()
        points[i] = list(map(float, tokens))
    
    p75, p25 = np.percentile(points[:,0], [99.9, 0.1])
    points = points[points[:, 0] < p75]
    points = points[points[:, 0] > p25]
    x_max = np.max(points[:,0])
    x_min = math.floor(np.min(points[:,0]))
    
    p75, p25 = np.percentile(points[:,2], [99.9, 0.1])
    points = points[points[:, 2] < p75]
    points = points[points[:, 2] > p25]
    z_max = np.max(points[:,2])
    z_min = math.floor(np.min(points[:,2]))
    print(x_max,z_max)
    print(x_min,z_min)

    pointNum = points.shape[0]
    grid = np.zeros((200,200))
    for i in range(pointNum):
        x,y,z= points[i].astype(int)
        x=x//3 + abs(x_min)//3
        z=z//3 + abs(z_min)//3
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
    cv2.imshow("window", grid)
    cv2.waitKey(0)
    cv2.imwrite("test.png")
