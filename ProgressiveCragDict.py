

#let a unique combination of values in an area be called a crag, as in an outcropping of rock that you would recognize while navigating. a crag is a particular set of values for a rectangular grid of any size. If a crag _a_ is equal to "[[1]]" and a terrain _terry_ is equal to [[0,0],[0,1]], then _terry_ contains _a_.




rectanglesIter = lambda sMax: ((a,b) for s in range(1,sMax+1) for a in range(1,s+1) for b in range(1,s+1) if a==s or b==s)

deduplicate = lambda arr: [item for (i,item) in enumerate(arr) if i==0 or item not in arr[:i]]

intersect = lambda arr1, arr2: [item for item in arr1 if item in arr2]

bitArrToString = lambda bitArr: "".join("1" if val else "0" for val in bitArr)
stringToBitArr = lambda string: [char=="1" for char in string]


existentCrags = []
cragExistenceBits = []
terrain = []

    

def terrainContainsCrag(crag): #seems to work.
  terrainH, terrainW = len(terrain), len(terrain[0])
  cragH, cragW = len(crag), len(crag[0])
  assert cragH <= terrainH and cragW <= terrainW
  """for y in range(0,terrainH-cragH):
    for x in range(0,terrainW-cragW):
      for yCheck in range(cragH):
        for xCheck in range(cragW):
          if terrain[y+yCheck][x+xCheck] != crag[yCheck][xCheck]:
            pass"""
  for (x,y) in ((x,y) for y in range(terrainH-cragH+1) for x in range(terrainW-cragW+1)):
    #print("checking " + str((x,y)) + "...")
    found = True
    for (xCheck,yCheck) in ((xCheck,yCheck) for yCheck in range(cragH) for xCheck in range(cragW)):
      #this could have been 4 nested loops instead of 2, but the 2-loop version allows breaking and continuing in a cleaner way.
      if terrain[y+yCheck][x+xCheck] != crag[yCheck][xCheck]:
        found = False
        break #the crag does not exist at this (x,y), so move on to the next one.
    if found:
      return True
  return False
  

def possibleCrags(w,h,existentCrags): #seems to work for 2x2.
  #print("possibleCrags("+str(w)+","+str(h)+","+str(existentCrags)+")")
  assert w > 0 and h > 0
  if w==1 and h==1:
    #print("possibleCrags is running in 0d mode.")
    result = [[[0]],[[1]]]
    #print("possibleCrags is returning " + str(result) + "...")
    return result
  assert not (w==1 and h==1)
  if w<=2 and h<=2 and (w==1 or h==1):
    #print("possibleCrags is running in 1d tiny mode.")
    assert not (w==1 and h==1)
    existentCellVals = [crag[0][0] for crag in existentCrags if len(crag)==1 and len(crag[0])==1]
    if w==1:
      assert not h == 1
      result = [[[a],[b]] for a in existentCellVals for b in existentCellVals]
      #print("possibleCrags is returning " + str(result) + "...")
      return result
    elif h==1:
      assert not w == 1
      result = [[[a,b]] for a in existentCellVals for b in existentCellVals]
      #print("possibleCrags is returning " + str(result) + "...")
      return result
    else:
      assert False
  #print("possibleCrags did not use 0d mode or 1d tiny mode.")
  result = []
  genHorizCrags = lambda: (crag for crag in existentCrags if len(crag)==h-1 and len(crag[0])==w) #generator for finding crags in existentCrags where height==h-1 and width==w.
  genVertCrags = lambda: (crag for crag in existentCrags if len(crag)==h and len(crag[0])==w-1) #generator for finding crags in existentCrags where height==h and width==w-1.
  #print("genHorizCrags(): " + str([item for item in genHorizCrags()]))
  #print("genVertCrags(): " + str([item for item in genVertCrags()]))
  if w==1 or h==1:
    #print("possibleCrags is running in 1d mode.")
    assert not (w==1 and h==1)
    if w==1:
      assert not h == 1
      for topCrag in genHorizCrags():
        candidate = [[row[0]] for row in topCrag]+[[None]]
        #print("found candidate " + str(candidate))
        tipVals = []
        for bottomCrag in genHorizCrags():
          if [row[0] for row in bottomCrag[:-1]]==[row[0] for row in candidate[1:-1]]:
            tipVals.append(bottomCrag[-1][0])
        #print("tipVals is " + str(tipVals) + " before deduplication.")
        tipVals = deduplicate(tipVals)
        #print("tipVals is " + str(tipVals) + " after deduplication.")
        for tipVal in tipVals:
          #print("candidate was " + str(candidate) + ".")
          candidate[-1][-1] = tipVal
          #print("candidate is now " + str(candidate) + ".")
          assert not candidate in result
          result.append([[cell for cell in row] for row in candidate])
    elif h==1:
      assert not w == 1
      for leftCrag in genVertCrags():
        candidate = [[cell for cell in leftCrag[0]]+[None]]
        #print("found candidate " + str(candidate))
        tipVals = []
        for rightCrag in genVertCrags():
          if rightCrag[0][:-1]==candidate[0][1:-1]:
            tipVals.append(rightCrag[0][-1])
        #print("tipVals is " + str(tipVals) + " before deduplication.")
        tipVals = deduplicate(tipVals)
        #print("tipVals is " + str(tipVals) + " after deduplication.")
        for tipVal in tipVals:
          #print("candidate was " + str(candidate) + ".")
          candidate[-1][-1] = tipVal
          #print("candidate is now " + str(candidate) + ".")
          assert not candidate in result
          result.append([[cell for cell in row] for row in candidate])
    else:
      assert False
    #print("possibleCrags is returning " + str(result) + "...")
    return result
  #print("possibleCrags is running in 2d mode.")
  assert w != 1 and h !=1
  for topCrag in genHorizCrags():
    for leftCrag in genVertCrags():
      if [row[:-1] for row in topCrag]==leftCrag[:-1]:
        candidate = [[cell for cell in row] for row in topCrag] + [[cell for cell in leftCrag[-1]]+[None]]
        #print("found candidate " + str(candidate))
        #candidate does not include any information about its bottom right cell. we will further evaluate it to see what possible values the bottom right cell could have, and add a version of this candidate for each of those values.
        vertCornerVals = [] #values of the bottom right cell that are allowed by vertical crag checks.
        horizCornerVals = [] #ditto.
        for bottomCrag in genHorizCrags():
          #print("testing bottomCrag " + str(bottomCrag))
          if (len(bottomCrag)==1 or bottomCrag[:-1]==candidate[1:-1]) and bottomCrag[-1][:-1]==candidate[-1][:-1]:
            horizCornerVals.append(bottomCrag[-1][-1])
        for rightCrag in genVertCrags():
          #print("testing rightCrag " + str(rightCrag))
          if (rightCrag[:-1]==[row[1:] for row in candidate[:-1]]) and (len(rightCrag[-1])==1 or rightCrag[-1][:-1]==candidate[-1][1:-1]):
            vertCornerVals.append(rightCrag[-1][-1])
            #speed this up dramatically by only checking rightCrags whose bottom right cell is already in horizCornerVals.
            #speed this up by deduplicating as we go or having a special case for binary cell values.
        #print("vertCornerVals are " + str(vertCornerVals) + " before dedupe.")
        #print("horizCornerVals are " + str(horizCornerVals) + " before dedupe.")
        vertAllowableCornerVals = deduplicate(vertCornerVals) #slow
        horizAllowableCornerVals = deduplicate(horizCornerVals) #slow
        #print("vertCornerVals are " + str(vertCornerVals) + " after dedupe.")
        #print("horizCornerVals are " + str(horizCornerVals) + " after dedupe.")
        for cornerVal in intersect(vertCornerVals,horizCornerVals):
          #print("processing cornerVal " + str(cornerVal) + "...")
          candidate[-1][-1] = cornerVal #with the bottom right cell of candidate being all possible values...
          assert not candidate in result
          result.append([[cell for cell in row] for row in candidate]) #save a copy of candidate to result.
  #print("checking for errors...")
  for candidate in result: #this should not be necessary.
    if candidate in existentCrags:
      print(str(candidate) + " was in " + str(existentCrags) + ".")
      print(raw_input("read error. press enter."))
    for row in candidate:
      for cell in row:
        if cell==None:
          print("a cell was None.")
          print(raw_input("read error. press enter."))
  #print("possibleCrags is returning " + str(result) + "...")
  return result


def doDNA(mode):
  assert mode in ["encode","decode"]
  maxRectangleSide = min(len(terrain),len(terrain[0]))
  if mode=="encode":
    for (w,h) in rectanglesIter(maxRectangleSide):
      for crag in possibleCrags(w,h,existentCrags):
        exists = terrainContainsCrag(crag)
        #print("crag=" + str(crag) + ", exists=" + str(exists) + ".")
        if exists:
          cragExistenceBits.append(True)
          existentCrags.append(crag)
        else:
          cragExistenceBits.append(False)
  elif mode=="decode":
    i = 0 #the index of the bit to check.
    for (w,h) in rectanglesIter(maxRectangleSide):
      for crag in possibleCrags(w,h,existentCrags):
        if len(cragExistenceBits)<=i:
          print("doDNA(\"decode\"): error: ran out of cragExistenceBits while decoding. returning...")
          return
        if cragExistenceBits[i]==True:
          existentCrags.append(crag)
        i += 1
  else:
    assert False
    
    
    
    

