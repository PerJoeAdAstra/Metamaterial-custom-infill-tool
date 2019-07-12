def generateArrowheadPoints(scale, height, width, angle, rads=1, xoffset=0):
  w = width * scale
  h = height * scale
  if rads:
    theta = angle
  else:
    theta = math.radians(angle)

  y_short           = w * math.tan(theta)
  x_offset          = 0

  if y_short > h:
    print("Error, undrawable shape! y_short:", y_short, " > h:", h)
    return list()

  shape = list()
  x=0
  ax = [x + xoffset/2, x + w - xoffset/2]
  y = 0
  shape.append((round(ax[1]), round(y)))
  shape.append((round(ax[0]), round(y - y_short)))
  shape.append((round(ax[1]), round(y + h)))
  return shape

def generateReentrantPoints(scale, height, width, angle, rads=1, xoffset=0):
    w = width * scale
    h = height * scale
    if rads:
        theta = angle
    else:
        theta = math.radians(angle)

    hex_side          = h
    hex_width         = w * 2

    hex_height        = hex_side * 2
    pattern_height    = hex_height + hex_side
    y_short           = w * math.tan(theta)

    if y_short > hex_side:
        print("Error, undrawable shape! y_short:", y_short, " > hex_side:", hex_side)
        return list()

    shape = list()
    ax = [0, 0 + w]
    shape.append((round(ax[1]), round(0)))
    shape.append((round(ax[0]), round(0 - y_short)))
    shape.append((round(ax[0]), round(0 - y_short + hex_side)))
    shape.append((round(ax[1]), round(0 - y_short + hex_side - y_short)))
    shape.append((round(ax[1]), round(0 - y_short + hex_side - y_short + hex_side)))
    return shape

def generateSinusoidalPoints(amplitude, wavelength, rate=20):
    points = list()
    for i in range(rate):
        print(i)
        y = (2 * math.pi) * (i/rate) * wavelength
        x = amplitude * math.sin((2 * math.pi) * (i/rate))
        print(x, y, " rounded: ", round(x),round(y))
        points.append((round(x),round(y)))
    return points

def generateHexagonPoints(scale):
  distance = scale
  hex_side          = distance/(math.sqrt(3)/2)
  hex_width         = distance * 2

  hex_height        = hex_side * 2
  pattern_height    = hex_height + hex_side
  y_short           = distance * math.sqrt(3)/3

  shape = list()
  x=0
  ax = (x, x+distance)
  y = 0
  shape.append((round(ax[1]), round(y)))
  shape.append((round(ax[0]), round(y + y_short)))
  shape.append((round(ax[0]), round(y + y_short + hex_side)))
  shape.append((round(ax[1]), round(y + y_short + hex_side + y_short)))
  shape.append((round(ax[1]), round(y + y_short + hex_side + y_short + hex_side)))
  return shape

def generateHexStarPoints(scale, starHeight = 10, starOffset = 4):
    distance = scale
    hex_side          = distance/(math.sqrt(3)/2)
    hex_width         = distance * 2

    hex_height        = hex_side * 2
    pattern_height    = hex_height + hex_side
    y_short           = distance * math.sqrt(3)/3

    inShort = round(starOffset*math.sin(math.radians(30)))
    inLong = round(starOffset*math.cos(math.radians(30)))

    outLong = round(starHeight*math.cos(math.radians(30)))
    outShort = round(starHeight*math.sin(math.radians(30)))

    hex = list()
    shape = list()
    x=0
    ax = (x, x+distance)
    y = 0
    point = (round(ax[1]), round(y))
    shape.append((point[0], point[1] - starOffset))            #1
    shape.append((point[0] - outLong, point[1] - outShort))    #2
    shape.append((point[0] - inLong, point[1] + inShort))      #3
    shape.append((point[0], point[1] + starHeight))            #4
    shape.append((point[0] - inLong, point[1] + inShort))      #5

    point = (round(ax[0]), round(y + y_short))
    shape.append((point[0] + inLong, point[1] - inShort))
    shape.append((point[0], point[1] - starHeight))
    shape.append((point[0] + inLong, point[1] - inShort))
    shape.append((point[0] + outLong, point[1] + outShort))
    shape.append((point[0], point[1] + starOffset))

    point = (round(ax[0]), round(y + y_short + hex_side))
    shape.append((point[0], point[1] - starOffset))
    shape.append((point[0] + outLong, point[1] - outShort))
    shape.append((point[0] + inLong, point[1] + inShort))
    shape.append((point[0], point[1] + starHeight))
    shape.append((point[0] + inLong, point[1] + inShort))

    point = (round(ax[1]), round(y + y_short + hex_side + y_short))
    shape.append((point[0] - inLong, point[1] - inShort))
    shape.append((point[0], point[1] - starHeight))
    shape.append((point[0] - inLong, point[1] - inShort))
    shape.append((point[0] - outLong, point[1] + outShort))
    shape.append((point[0], point[1] + inShort))

    shape.append((round(ax[1]), round(y + y_short + hex_side + y_short + hex_side - inShort)))
    return shape
