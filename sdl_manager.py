white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

yellow = (255,255,0)
magenta = (255,0,255)
cyan = (0,255,255)

def drawSphere(radius, center, screenSize, render, col):
    for y in range(center[1]-radius+1, center[1]+radius):
        for x in range(center[0]-radius+1, center[0]+radius):
            if(x > 0 and x < screenSize[0] and y < screenSize[1] and y > 0):
                if(pow((x - center[0]),2) + pow((y - center[1]), 2) <= pow(radius,2)):
                    render.draw_point([x,y], sdl2.ext.Color(col[0],col[1],col[2]))

def clearScreen(render, screenSize, col=black, slowClear = False):
    for x in range(screenSize[0]):
        for y in range(screenSize[1]):
            render.draw_point([x,y], sdl2.ext.Color(col[0],col[1],col[2]))
        if slowClear:
            render.present()

def drawShape(shape, col, render, slowdraw=False):
    for index, point in enumerate(shape):
        drawLine(point, shape[(index + 1) % (len(shape))], render, col)
    if slowdraw:
        render.present()

def drawLine(a, b, render, col):
  dx = abs(a[0] - b[0])
  dy = abs(a[1] - b[1])
  size = max(dx, dy) + 1
  points = interpolate(a, b, size)
  for point in points:
    render.draw_point([point[0],point[1]], sdl2.ext.Color(col[0],col[1],col[2]))

def drawDottedLine(a, b, render, col, gap=2, draw=2):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    size = max(dx, dy) + 1
    points = interpolate(a, b, size)
    for point in points:
        distance = math.sqrt(pow(a[0] - point[0],2) + pow(a[1] - point[1],2))
        if distance % (gap + draw) < draw:
            render.draw_point([point[0],point[1]], sdl2.ext.Color(col[0],col[1],col[2]))

def interpolate(a, b, size):
  results = list()
  current = list(a)
  step0 = (b[0]-a[0]) / max(size, 1)
  step1 = (b[1]-a[1]) / max(size, 1)
  for i in range(0, size):
    results.append((round(current[0]), round(current[1])))
    current[0] = current[0] + step0
    current[1] = current[1] + step1
  return results

def drawMixedPath(path, render, col1 = white, col2 = green, slowdraw=False, drawDotted = False):
    for index, point in enumerate(path):
        if(index + 1 < len(path)):
          if(path[index + 1][0] == 1):
            drawLine(point[1], path[(index + 1)][1], render, col = col1)
          elif drawDotted:
            drawDottedLine(point[1], path[(index+1)][1], render, col = col2)
        if(slowdraw):
            render.present()

def drawPath(path, render, col, slowdraw=False, dotted = False):
  for index, point in enumerate(path):
    if(index + 1 < len(path)):
      if(not dotted):
        drawLine(point, path[(index + 1)], render, col)
      else:
        drawDottedLine(point, path[(index+1)], render, col)
      if(slowdraw):
        render.present()

def drawShapes(shapes, render, slowdraw=False):
  colour = 1
  for shape in shapes:
    if(colour):
      drawPath(shape, render, white, slowdraw=slowdraw)
    else:
      drawPath(shape, render, red, slowdraw=slowdraw)
    colour = not(colour)
  render.present()

def drawMixedShapes(shapes, render, slowdraw=False, drawDotted = True):
  colour = 1
  for shape in shapes:
    if(colour):
      drawMixedPath(shape, render, col1 = white, slowdraw=slowdraw, drawDotted=drawDotted)
    else:
      drawMixedPath(shape, render, col1 = red, col2=cyan, slowdraw=slowdraw, drawDotted = drawDotted)
    colour = not(colour)
  render.present()
