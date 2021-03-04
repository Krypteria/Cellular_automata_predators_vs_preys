from constants import *
from generalMethods import *


# ------------------------------------------------------------------------
# Predator methods
# ------------------------------------------------------------------------
def predatorGrowth(times, cells, y, x):
    if((cells[y][x] & YOUNGMASK) and times[y][x] < PREDATORGROWTHRATIO):
        cells[y][x] = A_PREDATOR
        pygame.draw.polygon(screen, RED_A, getRectangle(y, x), 0)

# ------------------------------------------------------------------------

def predatorReproduction(times, cells, action, preyCells, y, x):
    global PREYCELLS, PREDATORCELLS
    k = 1
    if(len(preyCells) >= PRE_REPRO_CONDITION):
        k = PRE_REPRO_RATE
    for i in range(0, k):
        newY, newX = random.choice(preyCells)
        preyCells.remove([newY, newX])
        cells[newY][newX], times[newY][newX]  = Y_PREDATOR, TIMEPREDATOR
        action[y][x], action[newY][newX] = 0, 0
        draw(getRectangle(y, x), getRectangle(newY, newX), RED_A, RED_Y)  
        PREDATORCELLS += 1
        PREYCELLS -= 1

def predatorMovement(times, cells, action, newStep, predatorType, y, x):
    newY, newX = random.choice(newStep)
    cells[newY][newX], times[newY][newX] = predatorType, times[y][x] #conservo el tiempo
    cells[y][x], times[y][x] = NOTHING, 0
    action[newY][newX] = 0
    if(predatorType & YOUNGMASK):
        draw(getRectangle(y, x), getRectangle(newY, newX), BLACK, RED_Y)
    elif(predatorType & ADULTMASK):
        draw(getRectangle(y, x), getRectangle(newY, newX), BLACK, RED_A)

def predatorNewStepSearch(cells, y, x):
    newStep = []
    for k in range (0, NEIGHBORS): #cambiar por comprehension
        newX = (x + NXCOORD[k]) % NX
        newY = (y + NYCOORD[k]) % NY
        if(cells[newY][newX] == NOTHING):
            newStep.append([newY, newX])
    return newStep

def predatorFoodSearch(cells, y, x):
    preyCells = []
    for k in range(0, NEIGHBORS):
        newX = (x + NXCOORD[k]) % NX
        newY = (y + NYCOORD[k]) % NY
        if(cells[newY][newX] != NOTHING and not (cells[newY][newX] & TYPEMASK)): #si ataco a una presa me multiplico
            preyCells.append([newY, newX])
    return preyCells

# ------------------------------------------------------------------------

def adultPredatorBehaviour(times, cells, action, y, x):
    preyCells = predatorFoodSearch(cells, y, x)
    if(preyCells):
        predatorReproduction(times, cells, action, preyCells, y, x)
    else:
        newStep = predatorNewStepSearch(cells, y, x)
        if(newStep):
            predatorMovement(times, cells, action, newStep, A_PREDATOR, y, x)
        else:
            pygame.draw.polygon(screen, RED_A, getRectangle(y, x), 0)


def youngPredatorBehaviour(times, cells, action, y, x):
    newStep = predatorNewStepSearch(cells, y, x)
    if(newStep):
        predatorMovement(times, cells, action, newStep, Y_PREDATOR, y, x)
    else:
        pygame.draw.polygon(screen, RED_Y, getRectangle(y, x), 0)

def predadorBehaviour(times, cells, action, y, x):
    global PREDATORCELLS
    if(action[y][x]):
        predatorGrowth(times, cells, y, x)
        if(times[y][x] <= 0): #si ha muerto
            cells[y][x], times[y][x] = NOTHING, 0
            PREDATORCELLS -= 1
        elif(cells[y][x] & YOUNGMASK):
            youngPredatorBehaviour(times, cells, action, y, x)
        elif(cells[y][x] & ADULTMASK):
            adultPredatorBehaviour(times, cells, action, y, x)

# ------------------------------------------------------------------------