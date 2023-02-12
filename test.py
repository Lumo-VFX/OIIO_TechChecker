import os
os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"
import cv2
import numpy

imgPath = ".\\testImages\\Overscan_Checkerboard.exr"
img = cv2.imread(imgPath,cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
cv2.imshow("image",img)
cv2.waitKey(0)
print(img.shape)
(h, w) = img.shape[:2]
print(h,w)

(b,g,r) = img[1,1]
'''
print("Pixel at (0, 0) - Red: {}, Green: {}, Blue: {}".format(r, g, b))
offset = -50
(b,g,r) = img[h+offset,w+offset]
print("Pixel at ({}, {}) - Red: {}, Green: {}, Blue: {}".format(h+offset,w+offset,r, g, b))

for x in range(0,w, 100):
	(b,g,r) = img[int(h/2),x]
	print("Pixel at ({}, {}) - Red: {}, Green: {}, Blue: {}".format(x,int(h/2),r, g, b))
	'''