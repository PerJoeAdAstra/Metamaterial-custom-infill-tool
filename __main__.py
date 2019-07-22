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

# Scale editor
#   Scale the path with option to join points. Either properly or all of the
#   points dependent on file type
# If filetype is not automatic, open path editor
#   Add scale zoom to editor?

# Draw chosen path (allow to re-edit?)
#   Output if chosen
def __main__():
    #Enter filename
    validFile = False
    if(len(sys.argv) == 1):
        filename = input("Please enter filename: ")
    else:
        filename = sys.argv[1]

    while not validFile:
        try:
            file = open(filename, "r")
            file.close()
            validFile = True
        except IOError:
            filename = input("Invalid filename, Please enter filename: ")
    #get filetype, automatically detect?
    type = detectFileType(filename)

    if(type == 0 or type == 1):
        shape = readMixedPoints(filename)
        print("-- Scaling pattern --")
        # Do some scaling here
        print("Press the Left and Right arrow keys to scale your pattern,")
        print("Press 1 to invert x axis and 2 to invert y axis")
        print("Press 3 to toggle between points/autodraw/autodraw and points")
        print("Press Enter when you are happy with the scale to Continue")
        print("Press escape to Quit")
        scaledShape = scaleMixedEditor(shape)
        if(scaledShape == 0):
            exit()
        mixedShape = scaledShape
    else:
        shape = readPoints(filename)
        print("-- Scaling pattern --")
        # Do some scaling here
        print("Press the Left and Right arrow keys to scale your pattern,")
        print("Press 1 to invert x axis and 2 to invert y axis")
        print("Press 3 to toggle between points/autodraw/autodraw and points")
        print("Press Enter when you are happy with the scale to Continue")
        print("Press escape to Quit")
        scaledShape = scaleEditor(shape)
        if scaledShape == 0:
            exit()
        print("")
        print("Connect the points to create your infill path(s)")
        print("")
        print("Press left and right arrow keys to change points, ")
        print("press enter to select the point or s to skip the point.")
        print("press z to undo.")
        mixedShape = editPattern(scaledShape)
        if(mixedShape == 0):
            exit()

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

    print("-- Drawing preview --")
    cornerise(mixedShape, calculateMixedPatternWidth(mixedShape)/2, calculateMixedPatternActualHeight(mixedShape)/2)
    if(len(mixedShape)<300):
        isSlowdraw = True
    else:
        isSlowdraw = False
    isMovelines = False
    print("Press '1' to toggle dotted move lines on or off")
    print("Press '2' to toggle slowdraw on or off")
    print("")
    print("Press Enter to close and save the pattern")
    print("Press Escape to close and NOT save the patter")
    print("- Drawing, slowdraw:", isSlowdraw, "movement lines:", isMovelines, "-")
    drawMixedShapes(mixedShapes, renderer, slowdraw=isSlowdraw, drawDotted=isMovelines)
    print("- Finished drawing -")
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
                    if (len(sys.argv) != 1):
                        outname = sys.argv[1] # take off the .txt
                    else:
                        outname = filename
                    outname = outname.split('.')[0] + "_out.txt"
                    print("Writing out to", outname)
                    invertX(mixedShape)
                    invertY(mixedShape)
                    writeMixedPoints(outname, mixedShape)
                    print("Exiting")
                    running = False

                elif event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    print("Exiting, no save")
                    running = False

if __name__ == "__main__":
    __main__()
