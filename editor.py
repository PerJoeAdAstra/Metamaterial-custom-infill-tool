import sdl2.ext
import gc
from pattern_calculations import *
from sdl_manager import *

def calculatePatternOffset(pattern):
    minX = min(pattern, key=lambda x: x[0])
    minY = min(pattern, key=lambda x: x[1])
    return (minX[0], minY[1])

def calculateMixedPatternOffset(pattern):
    minX = min(pattern, key=lambda x: x[1][0])
    minY = min(pattern, key=lambda x: x[1][1])
    return (minX[1][0], minY[1][1])

def centralisePattern(pattern, xoffset, yoffset):
    offset = calculatePatternOffset(pattern)
    centralisedPattern = list()
    for point in pattern:
        centralisedPattern.append((point[0] - offset[0] + xoffset, point[1] - offset[1] + yoffset))
    return centralisedPattern

def centraliseMixedPattern(pattern, xoffset, yoffset):
    offset = calculateMixedPatternOffset(pattern)
    centralisedPattern = list()
    for point in pattern:
        centralisedPattern.append((point[0],(point[1][0] - offset[0] + xoffset, point[1][1] - offset[1] + yoffset)))
    return centralisedPattern

def cornerise(pattern, xoffset, yoffset):
    centralPattern = centraliseMixedPattern(pattern, 0, 0)
    offset = calculateMixedPatternOffset(pattern)
    width = calculateMixedPatternWidth(pattern)
    height = calculateMixedPatternActualHeight(pattern)
    cornerisedPattern = list()
    for point in pattern:
        cornerisedPattern.append((point[0],roundt((point[1][0] + width/2, point[1][1] + height/2))))
    return cornerisedPattern

def highlightPoint(point, screenSize, render, pointCol, hilightCol, pointRad=2, highlightRad=2):
    drawSphere(highlightRad, roundt(point), screenSize, render, hilightCol)
    drawSphere(pointRad, roundt(point), screenSize, render, pointCol)

def removeBorder(pattern, border):
    borderlessPattern = list()
    for point in pattern:
        borderlessPattern.append((point[0] - int(border[0]/2), point[1] - int(border[1]/2)))
    return borderlessPattern

def removeMixedBorder(pattern, border):
    borderlessPattern = list()
    for point in pattern:
        borderlessPattern.append((point[0], (point[1][0] - int(border[0]/2), point[1][1] - int(border[1]/2))))
    return borderlessPattern

def getScale(pattern, scale):
    return scale/max(calculatePatternWidth(pattern), calculatePatternActualHeight(pattern))

def getMixedScale(pattern, scale):
    return scale/max(calculateMixedPatternWidth(pattern), calculateMixedPatternActualHeight(pattern))

def drawWithToggle(pattern, render, toggle, editorSize):
    clearScreen(render)
    if(toggle == 0):
        drawPath(pattern, render)
    elif(toggle == 1):
        drawPoints(pattern, render, editorSize)
    else:
        drawPoints(pattern, render, editorSize)
        drawPath(pattern, render)

def drawMixedWithToggle(pattern, render, toggle, editorSize):
    clearScreen(render)
    if(toggle == 0):
        drawMixedPath(pattern, render)
    elif(toggle == 1):
        drawMixedPoints(pattern, render, editorSize)
    else:
        drawMixedPoints(pattern, render, editorSize)
        drawMixedPath(pattern, render)

def scaleEditor(pattern, border = 100):
    scale = 200
    size = 500
    toggle = 1
    editorSize = (size + border, size + border)
    scaledPattern = scaleFromOrigin(getScale(pattern, scale), pattern)
    centralScaled = centralisePattern(scaledPattern, ((size+border) - calculatePatternWidth(scaledPattern))/2, ((size+border) - calculatePatternActualHeight(scaledPattern))/2)
    running = True
    editor = sdl2.ext.Window("PatternEditor", size=editorSize)
    editRenderer = sdl2.ext.Renderer(editor)
    editor.show()
    drawWithToggle(centralScaled, editRenderer, toggle, editorSize)
    editRenderer.present()
    newPattern = list()
    while running: #TODO - create a large window and let them scale their pattern. Add a "autoconnnect toggle to see it better"
        gc.collect()
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_LEFT:
                    if scale > 20:
                        scale -= 20
                    else:
                        print("Cannot scale smaller!")
                    scaledPattern = scaleFromOrigin(getScale(scaledPattern, scale), scaledPattern)
                    centralScaled = centralisePattern(scaledPattern, ((size+border) - calculatePatternWidth(scaledPattern))/2, ((size+border) - calculatePatternActualHeight(scaledPattern))/2)
                    clearScreen(editRenderer)
                    drawWithToggle(centralScaled, editRenderer, toggle, editorSize)
                elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    if scale < 500:
                        scale += 20
                    else:
                        print("Cannot scale larger!")
                    scaledPattern = scaleFromOrigin(getScale(scaledPattern, scale), scaledPattern)
                    centralScaled = centralisePattern(scaledPattern, ((size+border) - calculatePatternWidth(scaledPattern))/2, ((size+border) - calculatePatternActualHeight(scaledPattern))/2)
                    clearScreen(editRenderer)
                    drawWithToggle(centralScaled, editRenderer, toggle, editorSize)

                elif event.key.keysym.sym == sdl2.SDLK_1:
                    scaledPattern = invertX(scaledPattern)
                    centralScaled = centralisePattern(scaledPattern, ((size+border) - calculatePatternWidth(scaledPattern))/2, ((size+border) - calculatePatternActualHeight(scaledPattern))/2)
                    clearScreen(editRenderer)
                    drawWithToggle(centralScaled, editRenderer, toggle, editorSize)

                elif event.key.keysym.sym == sdl2.SDLK_2:
                    scaledPattern = invertY(scaledPattern)
                    centralScaled = centralisePattern(scaledPattern, ((size+border) - calculatePatternWidth(scaledPattern))/2, ((size+border) - calculatePatternActualHeight(scaledPattern))/2)
                    clearScreen(editRenderer)
                    drawWithToggle(centralScaled, editRenderer, toggle, editorSize)

                elif event.key.keysym.sym == sdl2.SDLK_3:
                    toggle = (toggle + 1)%3
                    drawWithToggle(centralScaled, editRenderer, toggle, editorSize)
                elif event.key.keysym.sym == sdl2.SDLK_RETURN:
                    running = False
                elif event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    print("Quit!")
                    scaledPattern = 0
                    running = False
        editRenderer.present()
    if scaledPattern != 0:
        return removeBorder(centralScaled, ((size+border) - calculatePatternWidth(scaledPattern), (size+border) - calculatePatternActualHeight(scaledPattern)))
    else:
        return 0

def scaleMixedEditor(pattern, border = 100):
    scale = 200
    size = 500
    toggle = 1
    editorSize = (size + border, size + border)
    scaledPattern = scaleMixedFromOrigin(getMixedScale(pattern, scale), pattern)
    centralScaled = centraliseMixedPattern(scaledPattern, ((size+border) - calculateMixedPatternWidth(scaledPattern))/2, ((size+border) - calculateMixedPatternActualHeight(scaledPattern))/2)
    running = True
    editor = sdl2.ext.Window("PatternEditor", size=editorSize)
    editRenderer = sdl2.ext.Renderer(editor)
    editor.show()
    drawMixedWithToggle(centralScaled, editRenderer, toggle, editorSize)
    editRenderer.present()
    newPattern = list()
    while running: #TODO - create a large window and let them scale their pattern. Add a "autoconnnect toggle to see it better"
        gc.collect()
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_LEFT:
                    if scale > 20:
                        scale -= 20
                    else:
                        print("Cannot scale smaller!")
                    scaledPattern = scaleMixedFromOrigin(getMixedScale(scaledPattern, scale), scaledPattern)
                    centralScaled = centraliseMixedPattern(scaledPattern, ((size+border) - calculateMixedPatternWidth(scaledPattern))/2, ((size+border) - calculateMixedPatternActualHeight(scaledPattern))/2)
                    clearScreen(editRenderer)
                    drawMixedWithToggle(centralScaled, editRenderer, toggle, editorSize)
                elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    if scale < 500:
                        scale += 20
                    else:
                        print("Cannot scale larger!")
                    scaledPattern = scaleMixedFromOrigin(getMixedScale(scaledPattern, scale), scaledPattern)
                    centralScaled = centraliseMixedPattern(scaledPattern, ((size+border) - calculateMixedPatternWidth(scaledPattern))/2, ((size+border) - calculateMixedPatternActualHeight(scaledPattern))/2)
                    clearScreen(editRenderer)
                    drawMixedWithToggle(centralScaled, editRenderer, toggle, editorSize)

                elif event.key.keysym.sym == sdl2.SDLK_1:
                    scaledPattern = invertMixedX(scaledPattern)
                    centralScaled = centraliseMixedPattern(scaledPattern, ((size+border) - calculateMixedPatternWidth(scaledPattern))/2, ((size+border) - calculateMixedPatternActualHeight(scaledPattern))/2)
                    clearScreen(editRenderer)
                    drawMixedWithToggle(centralScaled, editRenderer, toggle, editorSize)

                elif event.key.keysym.sym == sdl2.SDLK_2:
                    scaledPattern = invertMixedY(scaledPattern)
                    centralScaled = centraliseMixedPattern(scaledPattern, ((size+border) - calculateMixedPatternWidth(scaledPattern))/2, ((size+border) - calculateMixedPatternActualHeight(scaledPattern))/2)
                    clearScreen(editRenderer)
                    drawMixedWithToggle(centralScaled, editRenderer, toggle, editorSize)

                elif event.key.keysym.sym == sdl2.SDLK_3:
                    toggle = (toggle + 1)%3
                    drawMixedWithToggle(centralScaled, editRenderer, toggle, editorSize)
                elif event.key.keysym.sym == sdl2.SDLK_RETURN:
                    running = False
                elif event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    print("Quit!")
                    scaledPattern = 0
                    running = False
        editRenderer.present()
    if(scaledPattern != 0):
        return removeMixedBorder(centralScaled, ((size+border) - calculateMixedPatternWidth(scaledPattern), (size+border) - calculateMixedPatternActualHeight(scaledPattern)))
    else:
        return 0

def editPattern(pattern, border=100):
    size = 500
    editorSize = (round(calculatePatternWidth(pattern)) + border, round(calculatePatternActualHeight(pattern)) + border)
    editor = sdl2.ext.Window("PatternEditor", size=editorSize)
    editRenderer = sdl2.ext.Renderer(editor)
    editor.show()
    editRenderer.present()
    centralPattern = centralisePattern(pattern, int(border/2), int(border/2))
    completePath = False
    drawPoints(centralPattern, editRenderer, editorSize)

    processor = sdl2.ext.TestEventProcessor()
    # processor.run(editor)
    editRenderer.present()

    newPattern = list()
    running = True
    highlightIndex = 0
    highlightPoint(centralPattern[highlightIndex], editorSize, editRenderer, white, white)
    scale = 1
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_LEFT:
                    highlightIndex = (highlightIndex - 1) % len(centralPattern)
                    clearScreen(editRenderer)
                    drawPoints(centralPattern, editRenderer, editorSize)
                    drawMixedPath(newPattern, editRenderer)
                    if len(newPattern) != 0:
                        drawSpecialLine(newPattern[-1], centralPattern[highlightIndex], editRenderer)
                    highlightPoint(centralPattern[highlightIndex], editorSize, editRenderer, white, white)
                elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    highlightIndex = (highlightIndex + 1) % len(centralPattern)
                    clearScreen(editRenderer)
                    drawPoints(centralPattern, editRenderer, editorSize)
                    drawMixedPath(newPattern, editRenderer)
                    if len(newPattern) != 0:
                        drawSpecialLine(newPattern[-1], centralPattern[highlightIndex], editRenderer)
                    highlightPoint(centralPattern[highlightIndex], editorSize, editRenderer, white, white)
                elif event.key.keysym.sym == sdl2.SDLK_RETURN:
                    # remove from old pattern and add to new pattern, draw pattern
                    newPattern.append((1, centralPattern.pop(highlightIndex)))
                    clearScreen(editRenderer)
                    drawPoints(centralPattern, editRenderer, editorSize)
                    drawMixedPath(newPattern, editRenderer)
                    if(len(centralPattern) == 0):
                        running = False
                    else:
                        highlightIndex = highlightIndex % len(centralPattern)
                        if len(newPattern) != 0:
                            drawSpecialLine(newPattern[-1], centralPattern[highlightIndex], editRenderer)
                        highlightPoint(centralPattern[highlightIndex], editorSize, editRenderer, white, white)
                elif event.key.keysym.sym == sdl2.SDLK_s:
                    newPattern.append((0,centralPattern.pop(highlightIndex)))
                    clearScreen(editRenderer)
                    drawPoints(centralPattern, editRenderer, editorSize)
                    drawMixedPath(newPattern, editRenderer)
                    if len(newPattern) != 0:
                        drawSpecialLine(newPattern[-1], centralPattern[highlightIndex], editRenderer)
                    if(len(centralPattern) == 0):
                        running = False
                    else:
                        highlightIndex = highlightIndex % len(centralPattern)
                        highlightPoint(centralPattern[highlightIndex], editorSize, editRenderer, white, white)
                elif event.key.keysym.sym == sdl2.SDLK_z:
                    if(len(newPattern) > 0):
                        highlightPoint(centralPattern[highlightIndex], editorSize, editRenderer, red, white)
                        centralPattern.insert(highlightIndex, newPattern.pop(len(newPattern)-1)[1])
                        clearScreen(editRenderer)
                        drawPoints(centralPattern, editRenderer, editorSize)
                        if len(newPattern) != 0:
                            drawSpecialLine(newPattern[-1], centralPattern[highlightIndex], editRenderer)
                        drawMixedPath(newPattern, editRenderer)
                        highlightPoint(centralPattern[highlightIndex], editorSize, editRenderer, white, white)
                    else:
                        print("Cannot undo!")
                        # highlightIndex = highlightIndex % len(centralPattern)
                        highlightPoint(centralPattern[highlightIndex], editorSize, editRenderer, white, white)
                elif event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    print("Quit!")
                    running = False
                    newPattern = 0
        editRenderer.present()
    if newPattern != 0:
        newPattern = removeMixedBorder(newPattern, (border,border))
    return newPattern


def getMousePosition():
    x, y = ctypes.c_int(0), ctypes.c_int(0) # Create two ctypes values
    while(x.value == 0):
        # Pass x and y as references (pointers) to SDL_GetMouseState()
        buttonstate = sdl2.mouse.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
        # Return x and y as Python values
        return (x.value, y.value)
