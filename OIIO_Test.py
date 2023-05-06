import OpenImageIO as oiio
from OpenImageIO import ImageInput, ImageOutput
from OpenImageIO import ImageBuf, ImageSpec, ImageBufAlgo
import numpy as np
import re
import os
from pprint import pprint
from pathlib import Path

#filepath = ".\\testImages\\Overscan_Checkerboard.exr"
#filepath = ".\\testImages\\BlackBorder_Checkerboard.exr"
#filepath = ".\\testImages\\Underscan_Checkerboard.exr"
#filepath = ".\\testImages\\2PX_BlackBorder_Checkerboard.exr"
#filepath = ".\\testImages\\BL_BlackBorder_Checkerboard.exr"
#filepath = ".\\testImages\\OVFX_STmap_base_HD_1280x720.exr"
#filepath = ".\\testImages\\Invalid_Pixels.exr"
filepath = "./testImages/Overscan_Checkerboard/Overscan_Checkerboard.####.exr"
#filepath = r'F:\Projects\Current\Auto_Tech_Checker\testImages\Overscan_Checkerboard\Overscan_Checkerboard.0001.exr'

#inp = ImageInput.open(filepath)
#spec = inp.spec()
#pixels = inp.read_image(0,3)
#print(np.where(pixels.isnan))
#print(np.where(pixels == np.inf))
#print("The first pixel is", pixels[0][0])
#roi = spec.roi
#roi_full = spec.roi_full
#x = 0
#if roi.xbegin < 0:
#	x = -roi.xbegin

#print(x)
#print(inp.format_name())


#inp.close()
filepath = Path(os.path.abspath(filepath))

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

	return(result)
	inp.close()

def check_channels(path):
	result = {}
	inp = ImageInput.open(path)
	spec = inp.spec()
	result["channel_number"] = spec.nchannels
	result["channel_names"] = spec.channelnames

	inp.close()
	

	return(result)

def average_vertical_line(pixels,x,height,increment = 10):
	count = 0
	block = []
	pixel_count = 0
	for y in range(height):
		pixel = pixels[y][x]
		#print("Analizing pixel at: ",x,y)
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
		#print("Analizing pixel at: ",x,y)
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

def check_edges(path,lines = 5):
	inp = ImageInput.open(path)
	spec = inp.spec()
	fwidth = spec.full_width
	fheight = spec.full_height
	xres = spec.width
	yres = spec.height
	height = min(fheight,yres)
	width = min(fwidth,xres)
	pixels = inp.read_image(0,3) #Read RGB
	roi = spec.roi
	roi_full = spec.roi_full
	x_begin = 0
	if roi.xbegin < 0:
		x_begin = -roi.xbegin
	#
	y_begin = 0 
	if roi.ybegin < 0:
		y_begin = -roi.ybegin
	#
	#ANALYZE VERTICAL LINES
	#Start with Left Lines
	Left_Edge = True
	Right_Edge = True
	Top_Edge = True
	Bottom_Edge = True
	vertical_lines = []
	vertical_result = []
	for x in range(x_begin,x_begin+lines):
		vertical_lines.append(average_vertical_line(pixels,x,height))
	for i in range(1,len(vertical_lines)):
		line_result = True
		for b in range((len(vertical_lines[i]))):
			if vertical_lines[i-1][b] < 0.00001:
				line_result = False

			elif vertical_lines[i-1][b]*5 < vertical_lines[i][b]:
				line_result = False
		vertical_result.append(line_result)
	for v in vertical_result:
		Left_Edge = Left_Edge and v
	vertical_result = []
	#Right most lines
	vertical_lines = []
	for x in range(width-lines,width):
		vertical_lines.append(average_vertical_line(pixels,x,height))
	for i in range(0,len(vertical_lines)-1):
		line_result = True
		for b in range((len(vertical_lines[i]))):
			if vertical_lines[i+1][b] < 0.00001:
				line_result = False

			elif vertical_lines[i+1][b] > vertical_lines[i][b]*5:
				line_result = False
		vertical_result.append(line_result)
	#print(vertical_result)
	for v in vertical_result:
		Right_Edge = Right_Edge and v
	#
	# ANALYZE HORIZONTAL LINES
	#Start with Top lines
	horizontal_lines = []
	horizontal_result = []
	for y in range(y_begin,y_begin+lines):
		horizontal_lines.append(average_horizontal_line(pixels,y,width))
	for i in range(1,len(horizontal_lines)):
		line_result = True
		for b in range((len(horizontal_lines[i]))):
			if horizontal_lines[i-1][b] < 0.00001:
				line_result = False

			elif horizontal_lines[i-1][b]*5 < horizontal_lines[i][b]:
				line_result = False
		horizontal_result.append(line_result)
	for v in horizontal_result:
		Top_Edge = Top_Edge and v
	horizontal_result = []
	#Bottom Lines
	horizontal_lines = []
	for y in range(height-lines,height):
		horizontal_lines.append(average_horizontal_line(pixels,y,width))
		#print(y)
	for i in range(0,len(horizontal_lines)-1):
		line_result = True
		for b in range((len(horizontal_lines[i]))):
			if horizontal_lines[i+1][b] < 0.00001:
				line_result = False

			elif horizontal_lines[i+1][b] > horizontal_lines[i][b]*5:
				line_result = False
		horizontal_result.append(line_result)
		#print(line_result)
	#print(horizontal_result)
	for v in horizontal_result:
		Bottom_Edge = Bottom_Edge and v
	horizontal_result = []
	inp.close()

	#Build result
	result = {}
	result["left_edge"] = Left_Edge
	result["right_edge"] = Right_Edge
	result["top_edge"] = Top_Edge
	result["bottom_edge"] = Bottom_Edge
	total = True
	for k,v in result.items():
		total = total and v
	if total:
		result = {}
		result["edges"] = True
	else:
		result["edges"] = False

	return(result)

def check_invalid_pixels(path):
	result = {}
	inp = ImageInput.open(path)
	pixels = inp.read_image(0,3) #Read RGB
	#print(not np.any(np.isnan(pixels)))
	#print(np.all(np.isfinite(pixels)))
	#print(np.array(np.where(pixels<0)).size)
	inf = np.all(np.isfinite(pixels))
	nan = not np.any(np.isnan(pixels))
	negative = (np.array(np.where(pixels<0)).size == 0)
	result['inf'] = inf
	result['nan'] = nan
	result['negative'] = negative
	total = True
	for k,v in result.items():
		total = total and v
	if total:
		result = {}
		result["invalid_pixels"] = True
	else:
		result["invalid_pixels"] = False
	return(result)

def check_all(path):
	result = {}
	result.update(check_edges(path))
	result.update(check_channels(path))
	result.update(check_bbox(path))
	result.update(check_invalid_pixels(path))
	return(result)

def path_to_frames(path):
	frames = {}

	if "#" in str(path):
		folder,file_name = os.path.split(path)
		#re_pattern = r'{}'.format(file_name)
		re_pattern = re.sub("#+", "([0-9]+)", file_name)
		folder = os.path.abspath(folder)
		for f in os.listdir(folder):
			re_match = re.match(re_pattern,f)
			if re_match:
				frames[re_match[1]] = os.path.join(folder,f)
				#print(os.path.join(folder,f))
	return(frames)

def check_file_sequence(path):
	frames = path_to_frames(path)
	result = {}
	prev_frame_channels = False
	for frame , frame_path in frames.items():
		result[frame] = {}
		frame_path = frame_path.replace("\\","\\\\")
		frame_result = check_edges(frame_path)
		if len(frame_result) > 1:
			result[frame].update(frame_result)
		frame_result = check_bbox(frame_path)
		if len(frame_result) > 1:
			result[frame].update(frame_result)
		frame_result = check_invalid_pixels(frame_path)
		if len(frame_result) > 1:
			result[frame].update(frame_result)

		frame_result = check_channels(frame_path)
		if prev_frame_channels:
			if frame_result != prev_frame_channels:
				result[frame].update(frame_result)
		else:
			result[frame].update(frame_result)
		prev_frame_channels = frame_result




	result = {k: v for k, v in result.items() if v}
	pprint(result)
	return()


 
check_file_sequence(filepath)
#print(filepath)