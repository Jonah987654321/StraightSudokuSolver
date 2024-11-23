st = [
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, 1, None, None],
    [6, None, 8, None, 5, None, None, 4, None],
    [None, 5, None, 9, None, None, None, None, 3],
    [None, None, None, None, None, 2, 5, None, None],
    [None, 4, 1, None, None, None, None, None, 6],
    [None, None, None, None, None, None, None, None, None],
    [None, 2, None, None, None, 8, None, None, None],
    [None, None, None, None, None, None, None, 8, None],
]

bf = [
    [0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
]

def printBoard(data):
    for row in data:
        print(" ".join([("0" if x is None else str(x)) for x in row])+"\n")
    print("---------------------")

def calcAllStraights(data):
    ret = {"rows": [], "columns": []}
    def getFirstBlack(arr):
        for i in range(0, len(arr)):
            if arr[i] == 1:
                return i
        return None

    for x in range(0, len(data)):
        fbi = getFirstBlack(data[x])
        if fbi is None:
            ret["rows"].append({"index": x, "start": 0, "stop": len(data[0])-1})
        elif fbi > 0:
            ret["rows"].append({"index": x, "start": 0, "stop": fbi-1})

    for x in range(0, len(data[0])):
        fbi = getFirstBlack([data[y][x] for y in range(len(data))])
        if fbi is None:
            ret["columns"].append({"index": x, "start": 0, "stop": len(data)-1})
        elif fbi > 0:
            ret["columns"].append({"index": x, "start": 0, "stop": fbi-1})

    for rowIndex in range(0, len(data)):
        for fieldIndex in range(0, len(data[rowIndex])):
            if (data[rowIndex][fieldIndex] == 1):
                #In row:
                if fieldIndex != 8:
                    nbi = getFirstBlack(data[rowIndex][fieldIndex+1:])
                    if nbi is None:
                        ret["rows"].append({"index": rowIndex, "start": fieldIndex+1, "stop": len(data[0])-1})
                    elif nbi > 0:
                        ret["rows"].append({"index": rowIndex, "start": fieldIndex+1, "stop": fieldIndex+nbi})

                #In column
                if rowIndex != 8:
                    nbi = getFirstBlack([data[y][fieldIndex] for y in range(len(data))][rowIndex+1:])
                    if nbi is None:
                        ret["columns"].append({"index": fieldIndex, "start": rowIndex+1, "stop": len(data)-1})
                    elif nbi > 0:
                        ret["columns"].append({"index": fieldIndex, "start": rowIndex+1, "stop": rowIndex+nbi})
        
    return ret

straights = calcAllStraights(bf)

def replaceFirstEmpty(list, new, rowIndex):
    global bf
    for x in range(0, len(list)):
        if list[x] is None and bf[rowIndex][x] == 0:
            list[x] = new
            break
    return list

def checkColumnsPossible(data):
    for x in range(0, len(data[0])):
        found = []
        for y in range(0, len(data)):
            if data[y][x] in found and data[y][x] is not None:
                return False
            found.append(data[y][x])
    return True

def checkStraightsPossible(data):
    global straights

    for s in straights["rows"]:
        sData = data[s["index"]][s["start"]:s["stop"]+1]
        amount = len(sData)
        sData = [x for x in sData if x is not None]
        if len(sData) > 0 and max(sData)-min(sData)+1 > amount:
            return False
        
    for s in straights["columns"]:
        sData = [data[x][s["index"]] for x in range(0, len(data))][s["start"]:s["stop"]+1]
        amount = len(sData)
        sData = [x for x in sData if x is not None]
        if len(sData) > 0 and max(sData)-min(sData)+1 > amount:
            return False
        
    return True

def rowHasEmpty(row, rowIndex):
    global bf

    for x in range(0, len(row)):
        if row[x] is None and bf[rowIndex][x] == 0:
            return True
    return False

possibles = []

queue = [st]

while len(queue) > 0:
    task = queue[0]
    replaced = False
    for x in range(0, len(task)):
        row = task[x]
        if rowHasEmpty(row, x):
            queue.pop(0)
            posRow = list(range(1, 10))
            for np in [y for y in row if y is not None]:
                posRow.remove(np)
            for p in posRow:
                newTask = task.copy()
                newTask[x] = replaceFirstEmpty(row.copy(), p, x)
                if checkColumnsPossible(newTask) and checkStraightsPossible(newTask):
                    queue.insert(0, newTask)
            replaced = True
            break
    
    if not replaced:
        queue.pop(0)
        possibles.append(task)

for p in possibles:
    printBoard(p)
