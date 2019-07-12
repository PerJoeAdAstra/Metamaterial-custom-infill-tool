import sdl2.ext
import os
import sys

from file_manager import *
from pattern_calculations import *
from premade_patterns import *
from sdl_manager import *
from editor import *


#for mouse position
import ctypes

import math
from random import randint

os.environ["PYSDL2_DLL_PATH"] = "/Python34/Lib/site-packages/PySDL2-0.9.3"

sdl2.ext.init()

# Global vairables -------------------------------------------------------------
screen_width = 500
screen_height = 500

mainScreenSize = (screen_width, screen_height)

#defining colours
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

yellow = (255,255,0)
magenta = (255,0,255)
cyan = (0,255,255)

center = (screen_width/2, screen_height/2)


# defining functions -----------------------------------------------------------

def drawThickLine(p1, p2, radius, render, col, endtype=round):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    rec = -1/(dx/dy)


    yintercept = p1[1] - rec * p1[0]

    a = (1 + pow(2, rec))
    b = 2 * rec * c
    c = pow(2, yinter) - pow(2, radius)

    p11 = (round((-b + math.sqrt(pow(b,2) - 4*a*c))/(2*a)), round(rec*x1 + yinter))
    p12 = (round((-b - math.sqrt(pow(b,2) - 4*a*c))/(2*a)), round(rec*x2 + yinter))

    yintercept = p1[1] - rec * p1[0]

    a = (1 + pow(2, rec))
    b = 2 * rec * c
    c = pow(2, yinter) - pow(2, radius)

    p21 = (round((-b + math.sqrt(pow(b,2) - 4*a*c))/(2*a)), round(rec*x1 + yinter))
    p22 = (round((-b - math.sqrt(pow(b,2) - 4*a*c))/(2*a)), round(rec*x2 + yinter))

    points = interpolate(a, b, size)
    for point in points:
        render.draw_point([point[0],point[1]], sdl2.ext.Color(col[0],col[1],col[2]))

def scaleFromOrigin(scale, shape):
    scaledShape = list()
    for point in shape:
        scaledShape.append((point[0] * scale, point[1] * scale))
    return scaledShape

def scaleMixedFromOrigin(scale, shape):
    scaledShape = list()
    for point in shape:
        scaledShape.append((point[0],(point[1][0] * scale,point[1][1] * scale)))
    return scaledShape

# script -----------------------------------------------------------------------

# test()

screenOn = True

scale = 20
height = 1
width = 1
angle = 10

# drawShapes(shapes)
# shapes = drawHexagons(scale)


# shapes1 = drawArrowhead(scale, height, width, angle, rads=0, xoffset=5)
# drawShapes(shapes1, slowdraw=True)

# reentrantPoints = generateReentrantPoints(scale, height, width, angle, rads=0)
# writePoints("reentrant.txt", reentrantPoints)
#
# arrowheadPoints = generateArrowheadPoints(scale, height, width, angle, rads=0)
# print(arrowheadPoints)
# print("-- generating points --")
# shape = generateHexStarPoints(scale)
# shape = generateSinusoidalPoints(scale, 10, rate = 50)

shape = readPoints("tired_dog0.txt")

print("-- editing points --")
mixedShape = editPattern(shape)

# writePoints("arrowhead.txt", arrowheadPoints)

# sinusoidalPoints = generateSinusoidalPoints(10, 10)
# writePoints("sinusoidal.txt", sinusoidalPoints)

# drawShape(sinusoidalPoints, white)
# shape = readMixedPoints("simpson1.txt")
# print(shape)
# writeMixedPoints("flower1.txt", shape)
# shape = readPoints("simpson.txt")
# shape = scaleFromOrigin(-2, shape)
# mixedShape = scaleMixedFromOrigin(-4, shape)
# shape = readPoints("sinusoidal.txt")
# print(shape)
# mixedShape = editPattern(shape)
if(screenOn):
    window = sdl2.ext.Window("Hello World!", size=(screen_width, screen_height))
    window.show()
    renderer = sdl2.ext.Renderer(window)
    renderer.present()



print("-- Tesselating shape --")
# print(calculateMixedPatternHeight(mixedShape), calculateMixedPatternWidth(mixedShape))
mixedShapes = tesselateMixedShape(mixedShape, calculateMixedPatternActualHeight(mixedShape), calculateMixedPatternWidth(mixedShape), isMirrored=False, connected=False)
print("--Finished!--")
drawMixedShapes(mixedShapes, renderer, slowdraw=True)

# tesselatedShape = tesselateShape(shape, 100, 100, isMirrored=False)
# drawShapes(tesselatedShape, renderer, slowdraw=True)

running = True
while running:
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            running = False
            break
        if event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_LEFT:
                print("Drawing, slow")
                clearScreen(renderer, mainScreenSize)
                drawMixedShapes(mixedShapes, renderer, slowdraw=True, drawDotted=True)
                print("Finished")

            elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                print("Drawing, quick")
                clearScreen(renderer, mainScreenSize)
                drawMixedShapes(mixedShapes, renderer, slowdraw=False, drawDotted=True)
                print("Finished")

            elif event.key.keysym.sym == sdl2.SDLK_UP:
                print("Drawing, slow - No dots")
                clearScreen(renderer, mainScreenSize)
                drawMixedShapes(mixedShapes, renderer, slowdraw=True, drawDotted=False)
                print("Finished")

            elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                print("Drawing, quick - No dots")
                clearScreen(renderer, mainScreenSize)
                drawMixedShapes(mixedShapes, renderer, slowdraw=False, drawDotted=False)
                print("Finished")

            elif event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                print("Exiting")
                running = False
# sdl2.SDL_Delay(5000)
