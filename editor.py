def calculatePatternOffset(pattern):
    minX = min(pattern, key=lambda x: x[0])
    minY = min(pattern, key=lambda x: x[1])
    return (minX[0], minY[1])

def centralisePattern(pattern, xoffset, yoffset):
    offset = calculatePatternOffset(pattern)
    print("offset:", offset)
    centralisedPattern = list()
    for point in pattern:
        centralisedPattern.append((point[0] - offset[0] + xoffset, point[1] - offset[1] + yoffset))
    return centralisedPattern

def highlightPoint(point, screenSize, render, pointCol, hilightCol, pointRad=2, highlightRad=2):
    drawSphere(highlightRad, point, screenSize, render, hilightCol)
    drawSphere(pointRad, point, screenSize, render, pointCol)

def removeBorder(pattern, border):
    borderlessPattern = list()
    for point in pattern:
        borderlessPattern.append((point[0], (point[1][0] - int(border/2), point[1][1] - int(border/2))))
    return borderlessPattern

def editPattern(pattern, border=100):
    editorSize = (calculatePatternWidth(pattern) + border, calculatePatternActualHeight(pattern) + border)
    editor = sdl2.ext.Window("PatternEditor", size=editorSize)
    editor.show()
    editRenderer = sdl2.ext.Renderer(editor)
    # clear the screen
    # draw the points
    clearScreen(editRenderer, editorSize)
    # editRenderer.present()
    centralPattern = centralisePattern(pattern, int(border/2), int(border/2))
    completePath = False
    # while(completePath == False): # while no path chosen
    # print(centralPattern)
    for point in centralPattern:
        drawSphere(2, point, editorSize, editRenderer, red)

    processor = sdl2.ext.TestEventProcessor()
    processor.run(editor)
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
                    highlightPoint(centralPattern[highlightIndex], editorSize, editRenderer, red, black)
                    highlightIndex = (highlightIndex - 1) % len(centralPattern)
                    highlightPoint(centralPattern[highlightIndex], editorSize, editRenderer, white, white)
                elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    highlightPoint(centralPattern[highlightIndex], editorSize, editRenderer, red, black)
                    highlightIndex = (highlightIndex + 1) % len(centralPattern)
                    highlightPoint(centralPattern[highlightIndex], editorSize, editRenderer, white, white)
                elif event.key.keysym.sym == sdl2.SDLK_RETURN:
                    print("Enter!")
                    # remove from old pattern and add to new pattern, draw pattern
                    highlightPoint(centralPattern[highlightIndex], editorSize, editRenderer, blue, black)
                    newPattern.append((1, centralPattern.pop(highlightIndex)))
                    drawMixedPath(newPattern, editRenderer)
                    if(len(centralPattern) == 0):
                        running = False
                    else:
                        highlightIndex = highlightIndex % len(centralPattern)
                        highlightPoint(centralPattern[highlightIndex], editorSize, editRenderer, white, white)
                elif event.key.keysym.sym == sdl2.SDLK_s:
                    print("Skip!")
                    highlightPoint(centralPattern[highlightIndex], editorSize, editRenderer, blue, black)
                    newPattern.append((0,centralPattern.pop(highlightIndex)))
                    drawMixedPath(newPattern, editRenderer)
                    if(len(centralPattern) == 0):
                        running = False
                    else:
                        highlightIndex = highlightIndex % len(centralPattern)
                        highlightPoint(centralPattern[highlightIndex], editorSize, editRenderer, white, white)
                elif event.key.keysym.sym == sdl2.SDLK_z:
                    print("Undo!")
                    print(len(newPattern))
                    if(len(newPattern) > 0):
                        highlightPoint(centralPattern[highlightIndex], editorSize, editRenderer, red, white)
                        drawMixedPath(newPattern, editRenderer, col1 = black)
                        centralPattern.insert(highlightIndex, newPattern.pop(len(newPattern)-1)[1])
                        drawMixedPath(newPattern, editRenderer)
                        highlightPoint(centralPattern[highlightIndex], editorSize, editRenderer, white, white)
                    else:
                        print("Cannot undo")
                        # highlightIndex = highlightIndex % len(centralPattern)
                        highlightPoint(centralPattern[highlightIndex], editorSize, editRenderer, white, white)
                elif event.key.keysym.sym == sdl2.SDLK_PLUS:
                    print("Enlarge!")
                elif event.key.keysym.sym == sdl2.SDLK_MINUS:
                    print("Reduce!")
                elif event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    print("Quit!")
                    running = False
        editRenderer.present()
    newPattern = removeBorder(newPattern, border)
    return newPattern


def getMousePosition():
    x, y = ctypes.c_int(0), ctypes.c_int(0) # Create two ctypes values
    while(x.value == 0):
        # Pass x and y as references (pointers) to SDL_GetMouseState()
        buttonstate = sdl2.mouse.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
        # Return x and y as Python values
        return (x.value, y.value)
