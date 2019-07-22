def echoFile(filename):
    print("-- reading file! --")
    with open(filename) as f:
        for line in f:
            print(line.splitlines()[0])
    f.close()

def readPattern(filename):
    print("-- Reading pattern --")
    pattern = list()
    with open(filename) as f:
        for line in f:
            line = line.splitlines()[0]
            pattern.append(line)
    return pattern

def writeLines(filename, lines):
    print("-- Writing pattern --")
    file = open(filename, "w+")
    for line in pattern:
        file.write(line + '\n')
    file.close()

def writePoints(filename, points):
    print("-- Writing points --")
    file = open(filename, "w+")
    for point in points:
        file.write(str(point[0]) + ',' + str(point[1]) + '\n')
    file.close()

def writeMixedPoints(filename, points):
    print("-- Writing formatted points -- ")
    file = open(filename, "w+")
    for point in points:
        file.write('(' + str(point[0]) + ',' + '(' + str(round(point[1][0])) + ',' + str(round(point[1][1])) + ')' + ')' + '\n')
    file.close()

def detectFileType(filename):
    file = open(filename, "r")
    firstLine = file.readline()
    if(firstLine[0] == '()'):                    #if first character of file is open bracket. Assume formatted mixed. return 0
        file.close()
        return 0
    for line in file:
        if line == '\n' or line == "#\n":
            file.close()
            return 1                             #otherwise check file for # or blank lines. If one is found return 1
    file.close()
    return 2                                     #otherwise return 2.

def readPoints(filename):
    print("-- Reading points --")
    file = open(filename, "r")
    pattern = list()
    for line in file:
        line = line.splitlines()[0]
        coord = line.split(',')
        pattern.append((int(coord[0]), int(coord[1])))
    return pattern

def readMixedPoints(filename, isConnected = True):
    print(" -- Reading formatted Points --")
    # Check if first character is a bracket, if so assume formatted
    file = open(filename, "r")
    pattern = list()
    firstline = file.readline()
    if firstline[0] == '(': # assume already in format
        firstline = firstline.replace('(', '')
        firstline = firstline.replace(')', '')
        firstline = firstline.splitlines()[0]
        coord = firstline.split(',')
        pattern.append((int(coord[0]), (int(coord[1]), int(coord[2]))))
        for line in file:
            line = line.replace('(', '')
            line = line.replace(')', '')
            line = line.splitlines()[0]
            coord = line.split(',')
            pattern.append((int(coord[0]), (int(coord[1]), int(coord[2]))))
        print("Formatted file")
    else: # assume not in format
        print("Non formatted file")
        firstline = firstline.splitlines()[0]
        coord = firstline.split(',')
        if(isConnected):
            pattern.append((1, (int(round(float(coord[0]))), int(round(float(coord[1]))))))
        else:
            pattern.append((0, (int(round(float(coord[0]))), int(round(float(coord[1]))))))
        toDraw = True
        for line in file:
            if(line == '\n' or line == "#\n"):
                toDraw = False
            else:
                line = line.splitlines()[0]
                coord = line.split(',')
                if toDraw:
                    pattern.append((1, (int(round(float(coord[0]))), int(round(float(coord[1]))))))
                else:
                    pattern.append((0, (int(round(float(coord[0]))), int(round(float(coord[1]))))))
                toDraw = True
    file.close()
    return pattern
