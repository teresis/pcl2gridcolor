""" generate random terrain-like 2D image

    (c) Volker Poplawski 2018
"""
from PIL import Image, ImageFilter
import random
import numpy as np

IMPASSABLE = 0.0
PASSABLE = 220


def generate_map(size, kernelsize, numiterations, path):
	#im = Image.new('RGB', (size, size), color=IMPASSABLE)
	gridmap = np.fromfile(path , dtype=np.float)
	gridsize = gridmap[:2].astype(int)
	grid = gridmap[2:]
	grid = np.reshape(grid, gridsize)
	grid = grid*220
	im = Image.fromarray(grid)
	im = im.resize((size,size))
    # init with random data
    #for x in range(0, im.width):
    #    for y in range(0, im.height):
    #        im.putpixel((x, y), random.choice([IMPASSABLE, PASSABLE]))

    # apply filter multiple times
    #for i in range(numiterations):
    #    im = im.filter(ImageFilter.RankFilter(kernelsize, kernelsize**2 // 2))

	return im




