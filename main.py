import sdl2.ext
import os
import sys
import gc

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

# script -----------------------------------------------------------------------

if(len(sys.argv) == 1):
    print("Please enter filename")

else:
    shape = readPoints(sys.argv[1])

    print("-- Editing points --")
    # Do some scaling here
    print("Press the + and - keys to scale your points,")
    print("they can be inverted with a negative scaling value")
    print("Press enter when you are happy with the scale")
    scaledShape = scaleEditor(shape)
    print("")
    print("Connect the points to create your infill path(s)")
    print("")
    print("Press left and right arrow keys to change points, ")
    print("press enter to select the point or s to skip the point.")
    print("press z to undo.")
    mixedShape = editPattern(scaledShape)

    print("-- Tesselating shape --")
    # print(calculateMixedPatternHeight(mixedShape), calculateMixedPatternWidth(mixedShape))
    mixedShapes = tesselateMixedShape(mixedShape, calculateMixedPatternActualHeight(mixedShape), calculateMixedPatternWidth(mixedShape), mainScreenSize, isMirrored=False, connected=False)
    print("--Finished Tesselating--")
    # tesselatedShape = tesselateShape(shape, 100, 100, isMirrored=False)
    # drawShapes(tesselatedShape, renderer, slowdraw=True)

    if(True):
        sdl2.ext.init()
        window = sdl2.ext.Window("Pattern Viewer", size=(screen_width, screen_height))
        window.show()
        renderer = sdl2.ext.Renderer(window)
        renderer.present()

    print("--Drawing preview--")
    isSlowdraw = True
    isMovelines = False
    drawMixedShapes(mixedShapes, renderer, slowdraw=isSlowdraw, drawDotted=isMovelines)
    print("Press '1' to toggle dotted move lines on or off")
    print("Press '2' to toggle slowdraw on or off")
    print("")
    print("Press Enter to close and save the pattern")
    print("Press Escape to close and NOT save the patter")

    running = True
    while running:
        gc.collect()
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_1:
                    clearScreen(renderer)
                    isMovelines = not isMovelines
                    print("- Drawing, slowdraw:", isSlowdraw, "movement lines:", isMovelines, "-")
                    drawMixedShapes(mixedShapes, renderer, slowdraw=isSlowdraw, drawDotted=isMovelines)
                    print("- Finished drawing -")

                elif event.key.keysym.sym == sdl2.SDLK_2:
                    clearScreen(renderer)
                    isSlowdraw = not isSlowdraw
                    print("- Drawing, slowdraw:", isSlowdraw, "movement lines:", isMovelines, "-")
                    drawMixedShapes(mixedShapes, renderer, slowdraw=isSlowdraw, drawDotted=isMovelines)
                    print("- Finished drawing -")

                elif event.key.keysym.sym == sdl2.SDLK_RETURN:
                    print("Writing out to", sys.argv[1] + "_out.txt")
                    writeMixedPoints(sys.argv[1] + "_out.txt", mixedShape)
                    print("Exiting")
                    running = False

                elif event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    print("Exiting, no save")
                    running = False
