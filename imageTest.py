image_dir = './assets/'
image_file = 'graph.png'
import cv2
import numpy as np
im = cv2.imread(image_dir + image_file, 1)
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) #(B)
im_blur = cv2.GaussianBlur(im_gray, (11, 11), 0) #(C)
ret1, th1 = cv2.threshold(im_blur, 127, 255, cv2.THRESH_BINARY_INV)
th2 = cv2.adaptiveThreshold(im_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 3)
#th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
cv2.imwrite('./output/graph_output.png', th2)
print(cv2.__version__)