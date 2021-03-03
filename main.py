import pygame
import numpy as np
import random
import time
pygame.font.init()

HEIGHT = 600
WIDTH = 900

GRAY = (125,125,125)
BLACK = (0, 0, 0)
RED = (200,30,30)   
WHITE = (255,255,255)

RED_A = (200,30,30) 
RED_Y = (255,51,135) 

GREEN_Y = (0,255,1)
GREEN_A = (19,126,19)
GREEN_O = (12,50,14)

RW = 10
RH = 10

NY = (int) (HEIGHT / RH)
NX = (int) (WIDTH / RW)

#CODIFICACIONES 

Y_PREDATOR = 0b1001
A_PREDATOR = 0b1010

Y_PREY = 0b0001
A_PREY = 0b0010


NOTHING = 0b0000

TIMEPREDATOR = 7
TIMEY_PREY = 9
TIMESIM = 0.3

PRE_REPRO_CONDITION = 3
PRE_REPRO_RATE = 2

PREY_VALUE = 27
PREDATOR_VALUE = 1

PREY_PERCENTAGE = PREY_VALUE / 100
PREDATOR_PERCENTAGE = PREDATOR_VALUE / 100
PREYCELLS = (int) (NX * NY * PREY_PERCENTAGE)
PREDATORCELLS = (int) (NX * NY * PREDATOR_PERCENTAGE)

PREYGROWTHRATIO = 4
PREDATORGROWTHRATIO = 3

#MASCARAS
TYPEMASK = 0b1000
EMPTYMASK = 0b0000
YOUNGMASK = 0b0001
ADULTMASK = 0b0010

FPS = 60

screen = pygame.display.set_mode([WIDTH, HEIGHT])
font = pygame.font.SysFont("arial", 20)

#Vectores de posicion
NEIGHBORS = 8
NYCOORD = [1,  1,  1, -1, -1, -1, 0 ,  0]
NXCOORD = [1,  0, -1,  1,  0, -1, 1 , -1]

# ------------------------------------------------------------------------
# General methods
# ------------------------------------------------------------------------

def getRectangle(y, x):
    return [(x * RW, y * RH), ((x + 1) * RW, y * RH), ((x + 1) * RW, (y + 1)* RH), (x * RW, (y + 1) * RH)]

def draw(source, nextStep, colorA, colorB):
    pygame.draw.polygon(screen, colorA, source, 0)
    pygame.draw.polygon(screen, colorB, nextStep, 0)

# ------------------------------------------------------------------------
# Y_Prey methods
# ------------------------------------------------------------------------

def preyGrowth(times, cells, y, x):
    if((cells[y][x] & YOUNGMASK) and times[y][x] < PREYGROWTHRATIO):
        cells[y][x] = A_PREY
        pygame.draw.polygon(screen, GREEN_A, getRectangle(y, x), 0)
        
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
# Predator methods
# ------------------------------------------------------------------------
def predatorGrowth(times, cells, y, x):
    if((cells[y][x] & YOUNGMASK) and times[y][x] < PREDATORGROWTHRATIO):
        cells[y][x] = A_PREDATOR
        pygame.draw.polygon(screen, RED_A, getRectangle(y, x), 0)

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
# Simulation management methods
# ------------------------------------------------------------------------

def redraw():
    preyLabel = font.render(f"Preys: {PREYCELLS}", 1, WHITE)
    predatorLabel = font.render(f"Predators: {PREDATORCELLS}", 1, WHITE)
    screen.blit(preyLabel, (10,10))
    screen.blit(predatorLabel, (10, 30))
    pygame.display.flip()


def runSimulation(times, cells, action):
    running = True
    paused = False
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                paused = not paused
        
        if(not paused):
            screen.fill(BLACK)
            time.sleep(TIMESIM)        
            for y in range (0, NY):
                for x in range (0, NX):
                    if (TYPEMASK & cells[y][x]): #PREDATOR
                        predadorBehaviour(times, cells, action, y, x)
                    elif((not (TYPEMASK & cells[y][x])) and (EMPTYMASK | cells[y][x] > 0)): #Y_PREY 
                        preyBehaviour(times, cells, action, y, x)
            redraw()     

            if(np.sum(cells) != 0):
                times = times - 1 #resto 1 tiempo a todas las celulas
                action = np.ones([NY, NX], dtype="int")

def initializeSimulation(times, cells):
    #TODO: generar elmentos totalmente diferentes, hay veces que se pisan unos a otros
    preyCount, predatorCount = PREYCELLS, PREDATORCELLS
    for i in range(0, PREYCELLS + PREDATORCELLS):
        y = np.random.randint(1, NY)
        x = np.random.randint(1, NX)
        rectangle = getRectangle(y, x)
        if(predatorCount and cells[y][x] == NOTHING):
            cells[y][x], times[y][x] = Y_PREDATOR, TIMEPREDATOR
            pygame.draw.polygon(screen, RED_Y, rectangle, 0)
            predatorCount -= 1
        elif(preyCount and cells[y][x] == NOTHING):
            cells[y][x], times[y][x] = Y_PREY, TIMEY_PREY
            pygame.draw.polygon(screen, GREEN_Y, rectangle, 0)
            preyCount -= 1

    print(predatorCount, " ", preyCount)
    pygame.display.flip()

def main():
    pygame.display.set_caption("Cellular automata")
    clock = pygame.time.Clock()
    clock.tick(FPS)
    screen.fill(BLACK)

    cells = np.zeros([NY, NX], dtype="int")
    times = np.zeros([NY, NX], dtype="int")
    action = np.ones([NY, NX], dtype="int")
    
    initializeSimulation(times, cells)
    runSimulation(times, cells, action)

                
if __name__ == "__main__":
    main()