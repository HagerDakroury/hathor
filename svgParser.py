from xml.dom import minidom
from svg.path import Move,Path, Line, Arc, CubicBezier, QuadraticBezier, Close,parse_path
import numpy as np

import serial
import struct

dimx=374.5
dimy=261.5
maxSpeed =20  #mm/sec

currentX=0
currentY=0
vx=[]
vy=[]
vz=[]
step=.1
scale=1

def generate_line(line):
    global currentX
    global currentY
    global vx
    global vy
    global scale

    currentX=line.start.real
    currentY=line.start.imag
    nextX=line.end.real
    nextY=line.end.imag

    vx.append((nextX-currentX)*scale)
    vy.append((nextY-currentY)*scale)
    currentX=nextX
    currentY=nextY

    vz.append(1)


#0->arc 1->CBezier 2->QBezier

def generate_curve(curve,type=3):
    global step
    global currentX
    global currentY
    global vx
    global vy
    global scale

    mySteps=np.arange(0.0,1.1,step)

    for i in mySteps:
        point=0

        if type==0:
            point = Arc.point(curve, i)
        if type == 1:
            point = CubicBezier.point(curve, i)
        if type == 2:
            point = QuadraticBezier.point(curve, i)


        nextX=point.real
        nextY=point.imag
        vx.append((nextX - currentX) * scale)
        vy.append((nextY - currentY) * scale)
        currentX = nextX
        currentY = nextY
        vz.append(1)

def generate_move(move):
    global currentX
    global currentY
    global vx
    global vy
    global scale


    nextX = move.end.real
    nextY = move.end.imag
    vx.append((nextX - currentX) * scale)
    vy.append((nextY - currentY) * scale)
    currentX = nextX
    currentY = nextY

    vz.append(0)



def generate(object):
    if isinstance(object,Line) or isinstance(object,Close):
        generate_line(object,)
    elif isinstance(object,Arc) :
        generate_curve(object,0)
    elif isinstance(object,CubicBezier):
        generate_curve(object,1)
    elif isinstance(object,QuadraticBezier):
        generate_curve(object,2)
    else:
        generate_move(object)

def test():
    global vx
    global vy
    global vz
    svg = open('test_car.svg')

    svg_dom = minidom.parse(svg)

    path_strings = [path.getAttribute('d') for path in svg_dom.getElementsByTagName('path')]

    for path_string in path_strings:
        path_data = parse_path(path_string)
#
    for path in path_data:
        generate(path)

    vx=[i for i in vx]
    vy=[i for i in vy]
    print(vx)





    return vx,vy,vz

#
# print (path_data)
# a=struct.pack('I',755)
# s = serial.Serial("COM5", 9600)
# #


#
# for i in vx:
#     a = struct.pack('I', vx)
#     s.write(a[0])
#     s.write(a[1])
