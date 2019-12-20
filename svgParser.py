from xml.dom import minidom
from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, Close,parse_path
import numpy as np
currentX=0
currentY=0
vx=[]
vy=[]
step=2
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

    vx.append(int((nextX-currentX)*scale))
    vy.append(int((nextY-currentY)*scale))
    currentX=nextX
    currentY=nextX

#0->arc 1->CBezier 2->QBezier
def generate_curve(curve,type=3):
    global step
    global currentX
    global currentY
    global vx
    global vy
    global scale

    mySteps=np.arange(0.0,1.0,step/curve.length())

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
        vx.append(int((nextX - currentX) * scale))
        vy.append(int((nextY - currentY) * scale))
        currentX = nextX
        currentY = nextX




def generate(object):
    if isinstance(object,Line) or isinstance(object,Close):
        generate_line(object,)
    if isinstance(object,Arc) :
        generate_curve(object,0)
    if isinstance(object,CubicBezier):
        generate_curve(object,1)
    if isinstance(object,QuadraticBezier):
        generate_curve(object,2)

svg = open('test_car.svg')

svg_dom = minidom.parse(svg)

path_strings = [path.getAttribute('d') for path in svg_dom.getElementsByTagName('path')]

for path_string in path_strings:
    path_data = parse_path(path_string)

for path in path_data:
    generate(path)

# for path_element in path_data:
#    print(path_element)
#
# l1=Line(100+100j,300+100j)
# print(Line.point(path_data[13],0.0))
#
# import serial
#
# s = serial.Serial("COM5", 9600)
#
# i=6789
# while(1):
#     s.write(str(i).encode("latin1"))
#
#     res = s.read()
#     print(int(res))
