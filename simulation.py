from svgParser import test
import numpy as np
import cv2

def resize (img,percentage):
    scale_percent = percentage  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

currentX=0
currentY=0
w=1000
h=600
img=np.zeros((1661,1703),np.uint8)
new=img.copy()
vx,vy,vz=test()
print(vx[2],vy[2])

#
for i in range (0,len(vx)):
    nextX=currentX+vx[i]
    nextY=currentY+vy[i]
    color=255 if vz[i] else 0
    new=cv2.line(new, (currentX, currentY), (nextX, nextY), (color, 0, 0), thickness=1)
    currentX=nextX
    currentY=nextY


cv2.imshow('h',resize(new,35))
cv2.waitKey(0)