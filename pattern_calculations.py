import math
def tesselateShape(inShape, height, width, isMirrored=True, xoffset=0):
    shapes = list()
    x = -width
    iter = 0
    while x < screen_width:
      shape = list()
      y = 0
      while y < screen_height:
          for point in inShape:
              if(isMirrored and iter%2==0):
                  shape.append((round(point[0] + x + iter * xoffset), round(point[1] + y)))
              else:
                  shape.append((round(x + iter * xoffset + width - point[0]), round(point[1] + y)))
          y+= height
      x += width
      iter += 1
      if(iter%2 == 1 and isMirrored):
          shape.reverse()
      shapes.append(shape)
    return shapes

def tesselateMixedShape(inShape, height, width, screenSize, isMirrored=True, xoffset=0, connected=True):
    shapes = list()
    x = 0
    iter = 0
    while x < screenSize[0]:
      shape = list()
      y = 0
      while y < screenSize[1]:
          first = True
          for point in inShape:
              if first and not connected:
                  shape.append((0,(round(point[1][0] + x + iter * xoffset), round(point[1][1] + y))))
                  first = False
              else:
                  if(isMirrored and iter%2==0):
                      shape.append((point[0],(round(x + iter * xoffset + width - point[1][0]), round(point[1][1] + y))))
                  else:
                      shape.append((point[0],(round(point[1][0] + x + iter * xoffset), round(point[1][1] + y))))
          y+= height
      x += width
      iter += 1
      # if(iter%2 == 1 and isMirrored):
      #     shape.reverse()
      shapes.append(shape)
    return shapes

def calculatePatternHeight(shape):
    return(abs(shape[0][1] - shape[-1][1]))

def calculatePatternActualHeight(shape):
    maxVal = max(shape, key=lambda x: x[1])       # find max y in list
    minVal = min(shape, key=lambda x: x[1])       # find min y in list
    return (abs(maxVal[1] - minVal[1]))

def calculateMixedPatternHeight(shape):
    return(abs(shape[0][1][1] - shape[-1][1][1]))

def calculateMixedPatternActualHeight(shape):
    maxVal = max(shape, key=lambda x: x[1][1])       # find max y in list
    minVal = min(shape, key=lambda x: x[1][1])       # find min y in list
    return (abs(maxVal[1][1] - minVal[1][1]))

def calculatePatternWidth(shape):
    maxVal = max(shape, key=lambda x: x[0])       # find max x in list
    minVal = min(shape, key=lambda x: x[0])       # find min x in list
    return (abs(maxVal[0] - minVal[0]))

def calculateMixedPatternWidth(shape):
    maxVal = max(shape, key=lambda x: x[1][0])       # find max x in list
    minVal = min(shape, key=lambda x: x[1][0])       # find min x in list
    return (abs(maxVal[1][0] - minVal[1][0]))

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

def invertX(shape, scale = -1):
    scaledShape = list()
    for point in shape:
        scaledShape.append((point[0] * scale,point[1]))
    return scaledShape

def invertY(shape, scale = -1):
    scaledShape = list()
    for point in shape:
        scaledShape.append((point[0], point[1] * scale))
    return scaledShape

def invertMixedX(shape, scale = -1):
    scaledShape = list()
    for point in shape:
        scaledShape.append((point[0],(point[1][0] * scale,point[1][1])))
    return scaledShape

def invertMixedY(shape, scale = -1):
    scaledShape = list()
    for point in shape:
        scaledShape.append((point[0],(point[1][0], point[1][1] * scale)))
    return scaledShape
