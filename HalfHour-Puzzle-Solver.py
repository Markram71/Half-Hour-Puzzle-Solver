##### Pink Cube Solver



# How full is the cube?
import copy 	#we need to copy elements
import sys 		#to end when we found the solution

#### Value #######
def valueOf(cube):
    n=0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                n=n+cube[i][j][k]
    return n



######## ROTATE ###########
# Rotate around Z axis
def rotateZ(element):
    r = copy.deepcopy(list(element))
    for i in range (1,len(r)):
        particle = element[i]
        x = particle[0]
        y = particle[1]
        z = particle[2]
        newPos = rotateMatrix[x][y]
        newDot = [newPos[0],newPos[1], z]
        r[i] = newDot
    return r
############
# Rotate around X axis
def rotateX(element):
    r = copy.deepcopy(list(element))
    for i in range (1,len(r)):
        particle = element[i]
        x = particle[0]
        y = particle[1]
        z = particle[2]
        newPos = rotateMatrix[y][z]
        newDot = [x, newPos[0],newPos[1]]
        r[i] = newDot
    return r
############
# Rotate around Z axis
def rotateY(element):
    r = copy.deepcopy(list(element))
    for i in range (1,len(r)):
        particle = element[i]
        x = particle[0]
        y = particle[1]
        z = particle[2]
        newPos = rotateMatrix[x][z]
        newDot = [newPos[0],y, newPos[1]]
        r[i] = newDot
    return r
############

###### Rotate Matrix
rotateMatrix =  (((2, 0), (1, 0), (0, 0)), ((2, 1 ), (1, 1), (0, 1)), ((2, 2), (1, 2), (0, 2)))

def printCube(cube):
	for x in range(3):
		for y in range(3):
			for z in range(3):
				print(cube[x][y][z], end='')
			print()
		print()


def fillRotateList(element):
	resultList =[]
	currentElementX = copy.deepcopy(list(element))
	x=0
	while x < 4:
		resultList.append(currentElementX)
		y=0
		currentElementY = copy.deepcopy(currentElementX)
		while y<4:
			resultList.append(currentElementY)
			z=0
			currentElementZ = copy.deepcopy(currentElementY)
			while z<4:
				resultList.append(currentElementZ)
				z+=1
				currentElementZ = rotateZ(currentElementZ)
			y+=1
			currentElementY = rotateY(currentElementY)	
		currentElementX = rotateX(currentElementX)
		x+=1
	return resultList

def areDotsEqual(dot1, dot2): #return true if both dots (in 3D space) are equal
	return dot1[0]==dot2[0] and dot1[1]==dot2[1] and dot1[2]==dot2[2]	

def removeDuplicates(rotateList):
	counter = 0
	#first step: identify the elements which are duplicates
	for m in range(len(rotateList)):
		firstElement = rotateList[m]
		for n in range(m+1,len(rotateList)):
			secondElement = rotateList[n]
			duplicateFound = True #we break and change when we find a difference 
			for l in range(1,len(firstElement)): # now check every dot in this element
				if not areDotsEqual(firstElement[l], secondElement[l]): duplicateFound = False
			#if not duplicateFound: print(duplicateFound, ":", firstElement, secondElement)
			if duplicateFound: firstElement[0] = 'X'
	#jetzt müssen wir noch die Duplicates löschen
	n= 0
	while n<len(rotateList):
		if rotateList[n][0] == 'X':
			del rotateList[n]
			counter+=1
		else: n+=1
	return counter
	
def removeAllDuplicates(superList):
	for n in range(len(superList)):
		print(n, ":", len(superList[n]), " rotated elements")
		duplicates = removeDuplicates(superList[n])
		print(duplicates)
		print(n, ":", len(superList[n]), " rotated elements")
		

# Insert an element into the cube, but only if it that is possible
positiveInsertions = 0 #global variable to track #of insertions
negativeInsertions = 0
def insertIntoCube(cube, element, xOffset, yOffset, zOffset):
	#let's first check if this is possible
	global positiveInsertions
	global negativeInsertions
	for n in range(1,len(element)):
		dot = element[n]
		x= dot[0] + xOffset
		y= dot[1] + yOffset
		z= dot[2] + zOffset
		if x<0 or y<0 or z<0 or x>2 or y>2 or z>2: return False
		if cube[x][y][z] != 0 : 
			negativeInsertions +=1
			return False
	#Ok, all cells are empty
	for n in range(1,len(element)):
		dot = element[n]
		x= dot[0] + xOffset
		y= dot[1] + yOffset
		z= dot[2] + zOffset
		cube[x][y][z] = element[0]
	positiveInsertions +=1
	return True


# REMOVE an element from a cube ----------
def removeFromCube (cube, element):
	code = element[0]
	for x in range(3):
		for y in range(3):
			for z in range(3):
				if cube[x][y][z] == code: cube[x][y][z] = 0

def recursiveAddElement(cube, superList, ElementPosition):
	#print(ElementPosition, end='')
	progress = 0 # how many rotations do we already have on level 0
	for rotatedElement in superList[ElementPosition]: #through all rotated puzzle pieces
		if ElementPosition==0: # give an overall update on the progress
			print()
			print(progress, " of ", len(superList[0]), ' : ', progress/len(superList[0]))
			print(rotatedElement)
			print("insertion status: ", positiveInsertions, " positiv / ", negativeInsertions, "negativ")
			progress +=1
		for x in range(-2,2):
			for y in range(-2,2):
				for z in range(-2,2):
					isPossible = insertIntoCube(cube,rotatedElement,x,y,z)
					if isPossible and ElementPosition == 5:
						print("Hurra!!!")
						printCube(cube)
						sys.exit() #We are done
					if isPossible and ElementPosition < 5: recursiveAddElement(cube, superList, ElementPosition + 1)
					removeFromCube(cube,rotatedElement)
	return True
														
print("Start of the Puzzle Solver")
print("Lets fill the rotate matrix")

###### Our Elements
emptyCube = [[[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]]]
el 		= ('a', (0,0,0),(0,1,0),(0,2,0),(1,0,0))#ok
tee  	= ('b', (0,0,0),(0,1,0),(0,2,0),(1,1,0))#ok
tee1 	= ('c', (0,0,0),(0,1,0),(0,2,0),(1,1,0),(1,1,1))#ok 
elPlus= ('d', (0,0,0),(0,1,0),(0,2,0),(1,2,0),(0,1,1))
ex   	= ('e', (0,0,0),(0,1,0),(1,1,0),(1,1,1))#ok
eli  	= ('f', (0,0,0),(0,1,0),(1,1,0),(1,2,0),(1,1,1))#ok
tester= ('g', (0,0,0),(0,1,0))


print("Let's fill our rotated lists'")
superList = [1,2,3,4,5,6,7] #Initialisierung
superList[0] = fillRotateList(eli)
superList[1] = fillRotateList(elPlus)
superList[2] = fillRotateList(tee1)
superList[3] = fillRotateList(tee)
superList[4] = fillRotateList(ex)
superList[5] = fillRotateList(el)
superList[6] = fillRotateList(tester)

print("All rotations filled up")
removeAllDuplicates(superList)
print("All duplicates removed")
print("----------------")
##### This is the main call to the puzzle solver
recursiveAddElement(emptyCube, superList, 0)


print("Oops, we are done, but did not find the solution, yet? Program is wrong or puzzle is wrong.")



