from constants import *
from generalMethods import *


# ------------------------------------------------------------------------
# Prey methods
# ------------------------------------------------------------------------

def preyGrowth(times, cells, y, x):
    if((cells[y][x] & YOUNGMASK) and times[y][x] < PREYGROWTHRATIO):
        cells[y][x] = A_PREY
        pygame.draw.polygon(screen, GREEN_A, getRectangle(y, x), 0)

# ------------------------------------------------------------------------        

def preyReproduction(times, cells, action, newStep, y, x):
    global PREYCELLS
    newY, newX = random.choice(newStep)
    newStep.remove([newY, newX])
    cells[newY][newX], times[newY][newX] = Y_PREY, TIMEY_PREY
    action[y][x], action[newY][newX] = 0, 0
    times[y][x] = TIMEY_PREY
    PREYCELLS += 1
    draw(getRectangle(y, x), getRectangle(newY, newX), GREEN_A, GREEN_Y)
    return newStep

def preyMovement(times, cells, action, newStep, preyType, y, x):
    newY, newX = random.choice(newStep)
    cells[newY][newX], times[newY][newX] = preyType, times[y][x]
    cells[y][x], times[y][x] = NOTHING, 0
    action[newY][newX] = 0

    if(preyType & YOUNGMASK):
        pygame.draw.polygon(screen, GREEN_Y, getRectangle(newY, newX), 0)
    elif(preyType & ADULTMASK):
        pygame.draw.polygon(screen, GREEN_A, getRectangle(newY, newX), 0)

def preyNewStepSearch(cells, y, x):
    newStep = []
    for k in range (0, NEIGHBORS): #cambiar por comprehension list
        newX = (x + NXCOORD[k]) % NX
        newY = (y + NYCOORD[k]) % NY
        if(cells[newY][newX] == NOTHING):
            newStep.append([newY, newX])
    return newStep

# ------------------------------------------------------------------------

def adultPreyBehaviour(times, cells, action, y, x):
    newStep = preyNewStepSearch(cells, y, x)
    if(newStep):
        if(times[y][x] <= 0):
            newStep = preyReproduction(times, cells, action, newStep, y, x) #quitar la posicion tomada de la lista
        if(newStep):
            preyMovement(times, cells, action, newStep, A_PREY, y, x)
    else:
        pygame.draw.polygon(screen, GREEN_A, getRectangle(y, x), 0)

def youngPreyBehaviour(times, cells, action, y, x):
    newStep = preyNewStepSearch(cells, y, x)
    if(newStep):
        preyMovement(times, cells, action, newStep, Y_PREY, y, x)
    else:
        pygame.draw.polygon(screen, GREEN_Y, getRectangle(y, x), 0)

def preyBehaviour(times, cells, action, y, x):
    if(action[y][x]):
        preyGrowth(times, cells, y, x)
        if(cells[y][x] & YOUNGMASK):
            youngPreyBehaviour(times, cells, action, y, x)
        elif(cells[y][x] & ADULTMASK):
            adultPreyBehaviour(times, cells, action, y, x)

# ------------------------------------------------------------------------