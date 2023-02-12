import oiio
from oiio import ImageInput, ImageOutput
from oiio import ImageBuf, ImageSpec, ImageBufAlgo
import numpy as np

filepath = ".\\testImages\\Overscan_Checkerboard.exr"
#filepath = ".\\testImages\\Underscan_Checkerboard.exr"

#filepath = ".\\testImages\\OVFX_STmap_base_2K_DCP_2048x1080.exr"

inp = ImageInput.open(filepath)
spec = inp.spec()
pixels = inp.read_image(0,3)
#print("The first pixel is", pixels[0][0])
roi = spec.roi
roi_full = spec.roi_full
print(roi.xbegin,roi_full.xbegin)
x = 0
if roi.xbegin < 0:
	x = -roi.xbegin

print(x)
#print(inp.format_name())

inp.close()


def check_bbox(path):
	result = {}
	inp = ImageInput.open(path)
	spec = inp.spec()
	xres = spec.width
	yres = spec.height
	fwidth = spec.full_width
	fheight = spec.full_height
	result["bbox"] = True
	if xres != fwidth:
		result["bbox"] = False
		result["bbox_width"] = []
		result["bbox_width"].append(False)
		if xres > fwidth:
			result["bbox_width"].append("Bbox width is bigger than format")
		else:
			result["bbox_width"].append("Bbox width is smaller than format")

	if yres != fheight:
		result["bbox"] = False
		result["bbox_height"] = []
		result["bbox_height"].append(False)
		if xres > fwidth:
			result["bbox_height"].append("Bbox height is bigger than format")
		else:
			result["bbox_height"].append("Bbox height is smaller than format")

	return([result["bbox"],result])
	inp.close()

def check_edges(path):
	result = {}
	inp = ImageInput.open(path)
	spec = inp.spec()
	fwidth = spec.full_width
	fheight = spec.full_height
	inp.close()
	pass

def check_channels(path):
	result = {}
	inp = ImageInput.open(path)
	spec = inp.spec()
	result["channel_number"] = spec.nchannels
	result["channel_names"] = spec.channelnames

	inp.close()
	

	return(result)


def check_edges(path,lines = 5):

	def average_vertical_line(pixels,x,height,increment = 10):
		count = 0
		block = []
		pixel_count = 0
		for y in range(height):
			pixel = pixels[y][x]
			pixel_avg = 0
			for v in pixel:
				pixel_avg = pixel_avg + v
			pixel_avg = pixel_avg / 3
			pixel_count = pixel_count + pixel_avg
			count += 1
			if not count % 10:
				block.append(pixel_count/10)
				pixel_count = 0
				count = 0 
		return(block)

	def average_horizontal_line(pixels,y,width,increment = 10):
		count = 0
		block = []
		pixel_count = 0
		for x in range(width):
			pixel = pixels[y][x]
			pixel_avg = 0
			for v in pixel:
				pixel_avg = pixel_avg + v
			pixel_avg = pixel_avg / 3
			pixel_count = pixel_count + pixel_avg
			count += 1
			if not count % 10:
				block.append(pixel_count/10)
				pixel_count = 0
				count = 0 
		return(block)

	inp = ImageInput.open(filepath)
	spec = inp.spec()
	fwidth = spec.width
	fheight = spec.height
	xres = spec.width
	yres = spec.height
	height = min(fheight,yres)
	width = min(fwidth,xres)
	pixels = inp.read_image(0,3) #Read RGB
	vertical_lines = []
	for x in range(lines):
		vertical_lines.append(average_vertical_line(pixels,x,height))
	for i in range(1,len(vertical_lines)):
		result = True
		for b in range((len(vertical_lines[i]))):
			if vertical_lines[i-1][b] < 0.00001:
				result = False

			if vertical_lines[i-1][b]*10 < vertical_lines[i][b]:
				result = False
		print(result)


	inp.close()





#check_edges(filepath)
