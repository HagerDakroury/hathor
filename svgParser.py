from xml.dom import minidom
from svg.path import Move,Path, Line, Arc, CubicBezier, QuadraticBezier, Close,parse_path
import numpy as np

import serial
import struct

dimx=374.5
dimy=261.5
maxFrequancy=32000.00
maxSpeed=0.00002

currentX=0
currentY=0
vx=[]
vy=[]
vz=[]
fx=[]
fy=[]
t=[]
dirx=[]
diry=[]
step=.05
scale=1
tRate=500


def resize(w, h):
    global vx
    global vy
    sW= float(dimx/w)
    sH=float(dimy/h)
    vx=[i*sW for i in vx]
    vy=[i*sH for i in vy]

def set_frequancy():
    global vx
    global vy
    global fx
    global fy
    global t

    for i in range(0,len(vx)):
        #direction assignment
        dirx.append(1 if vx[i] > 1 else 0)
        diry.append(1 if vy[i] > 1 else 0)
        vx[i]=abs(vx[i])
        vy[i]=abs(vy[i])

        if vx[i]==0 and vy[i]==0:
            fx.append(0)
            fy.append(0)
            t.append(0)
        elif vx[i]>vy[i]:
            fx.append(maxFrequancy)
            if vy[i]==0:
                fy.append(0)
            else:
                fy.append((vy[i] / vx[i]) * maxFrequancy)
            time = vx[i] / maxSpeed
            t.append(time)

        else:
            fy.append(maxFrequancy)
            if vx[i]==0:
                fx.append(0)
            else:
                fx.append((vx[i] / vy[i]) * maxFrequancy)
            time = vy[i] / maxSpeed
            t.append(time)


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

    mySteps=np.arange(0.0,1.05,step)

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

def load():
    global vx
    global vy
    global vz
    global fx
    global fy
    global t
    svg = open('simple.svg')

    svg_dom = minidom.parse(svg)

    path_strings = [path.getAttribute('d') for path in svg_dom.getElementsByTagName('path')]

    for path_string in path_strings:
        path_data = parse_path(path_string)


#
    for path in path_data:
        generate(path)

    vx=[i for i in vx]
    vy=[i for i in vy]
    w=float([path.getAttribute('width') for path in svg_dom.getElementsByTagName('svg')][0])
    h=float([path.getAttribute('height') for path in svg_dom.getElementsByTagName('svg')][0])

    resize(w,h)
    set_frequancy()
    fx = [int(i) for i in fx]
    fy = [int(i) for i in fy]
    t = [int(i) for i in t]




def transmit():
    global tRate
    i=0
    global fx
    global fy
    global t
    global dirx
    global diry
    global vz



    s = serial.Serial("COM4", 9600)


    while True :
        print(s.read())
        a = struct.pack('I', len(fx))
        s.write(a[0])
        s.write(a[1])
        s.write(a[2])
        s.write(a[3])


        while True:
            a = s.read()
            print(a)
            if a!='a':
                continue
            iold = i

            if i>len(fx)-1:
                break
            for j in range (i, iold+tRate):
                if j > len(fx) - 1:
                    break;
                ss = s.read()
                print(ss)
                a = struct.pack('I', fx[j])
                s.write(a[0])
                s.write(a[1])
                s.write(a[2])
                s.write(a[3])
                b = struct.pack('I', fy[j])
                s.write(b[0])
                s.write(b[1])
                s.write(b[2])
                s.write(b[3])
                t1=t[j]/1000
                t2=t[j]%1000
                c = struct.pack('I', t1)
                s.write(c[0])
                s.write(c[1])
                s.write(c[2])
                s.write(c[3])
                c = struct.pack('I', t2)
                s.write(c[0])
                s.write(c[1])
                s.write(c[2])
                s.write(c[3])

            for j in range(i, iold + tRate):
                # shifted_dirx=dirx[j]|dirx[j+1]<<1|dirx[j+2]<<2|dirx[j+3]<<3|dirx[j+4]<<4|dirx[j+5]<<5,dirx[j+6]<<6|dirx[j+7]<<7
                # shifted_diry=diry[j]|diry[j+1]<<1|diry[j+2]<<2|diry[j+3]<<3|diry[j+4]<<4|diry[j+5]<<5,diry[j+6]<<6|diry[j+7]<<7
                # shifted_pen=vz[j]|vz[j+1]<<1|vz[j+2]<<2|vz[j+3]<<3|vz[j+4]<<4|vz[j+5]<<5,vz[j+6]<<6|vz[j+7]<<7
                a = s.read()
                print(a)
                a = struct.pack('B', dirx[j])
                b = struct.pack('B', diry[j])
                c = struct.pack('B', vz[j])
                s.write(a[0])
                s.write(b[0])
                s.write(c[0])


load()
# print(sum(fx[0:499]))
# print(sum(fy[0:499]))
# print(sum(t[0:499]))
#
# print(sum(fx[0:999]))
# print(sum(fy[0:999]))
# print(sum(t[0:999]))

print(len(fx))
print(sum(fx))
print(sum(fy))
print(sum(t))

print(t)

transmit()


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
