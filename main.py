import pygame
import numpy as np
import random
import time

HEIGHT = 600
WIDTH = 900

GRAY = (125,125,125)
BLACK = (0, 0, 0)
GREEN = (48,138,52)
RED = (200,30,30)

RW = 10
RH = 10

NY = (int) (HEIGHT / RH)
NX = (int) (WIDTH / RW)

#CODIFICACIONES 
PREDATOR = 0b1010 
PREY = 0b0010
NOTHING = 0b0000

TIMEPREDATOR = 2
TIMEPREY = 1
TIMESIM = 0.1

PRE_REPRO_CONDITION = 3
PRE_REPRO_RATE = 2

#MASCARAS
TYPEMASK = 0b1000
EMPTYMASK = 0b0000

FPS = 60

screen = pygame.display.set_mode([WIDTH, HEIGHT])

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
# Prey methods
# ------------------------------------------------------------------------

def preyReproduction(times, cells, action, newStep, y, x):
    newY, newX = random.choice(newStep)
    cells[newY][newX], times[newY][newX] = PREY, TIMEPREY
    action[y][x], action[newY][newX] = 0, 0
    times[y][x] = TIMEPREY
    draw(getRectangle(y, x), getRectangle(newY, newX), GREEN, GREEN)

def preyMovement(times, cells, action,  newStep, y, x):
    newY, newX = random.choice(newStep)
    cells[newY][newX], times[newY][newX] = PREY, times[y][x]
    cells[y][x], times[y][x] = NOTHING, 0
    action[newY][newX] = 0
    draw(getRectangle(y, x), getRectangle(newY, newX), BLACK, GREEN)

def preyStep(times, cells, action, newStep, y, x):
    if(times[y][x] <= 0): #se reproduce
        preyReproduction(times, cells, action, newStep, y, x)
    else: #movimiento
        preyMovement(times, cells, action, newStep, y, x)

def preyRules(times, cells, action, y, x):
    newStep = []
    movimiento, reproduccion= False, False
    if(action[y][x]):
        for k in range (0, NEIGHBORS):
            newX = (x + NXCOORD[k]) % NX
            newY = (y + NYCOORD[k]) % NY
            if(cells[newY][newX] == NOTHING):
                newStep.append([newY, newX])

        if(newStep):
            preyStep(times, cells, action, newStep, y, x)
        else:
           pygame.draw.polygon(screen, GREEN, getRectangle(y, x), 0)

def preyBehaviour(times, cells, action, y, x):
    preyRules(times, cells, action, y, x)

# ------------------------------------------------------------------------
# Predator methods
# ------------------------------------------------------------------------

def predatorReproduction(times, cells, action, preyCells, y, x):
    k = 1
    if(len(preyCells) >= PRE_REPRO_CONDITION):
        k = PRE_REPRO_RATE
    for i in range(0, k):
        newY, newX = random.choice(preyCells)
        cells[newY][newX], times[newY][newX]  = PREDATOR, TIMEPREDATOR
        action[y][x], action[newY][newX] = 0, 0
        draw(getRectangle(y, x), getRectangle(newY, newX), RED, RED)  

def predatorMovement(times, cells, action, newStep, y, x):
    newY, newX = random.choice(newStep)
    cells[newY][newX], times[newY][newX] = PREDATOR, times[y][x] #conservo el tiempo
    cells[y][x], times[y][x] = NOTHING, 0
    action[newY][newX] = 0
    draw(getRectangle(y, x), getRectangle(newY, newX), BLACK, RED)

def predatorRules(times, cells, action, y, x):
    newStep = []
    preyCells = []
    if(action[y][x]):
        for k in range (0, NEIGHBORS):
            newX = (x + NXCOORD[k]) % NX
            newY = (y + NYCOORD[k]) % NY
            if(cells[newY][newX] == PREY): #si ataco a una presa me multiplico
                preyCells.append([newY, newX])
            elif(cells[newY][newX] == NOTHING):
                newStep.append([newY, newX])
        
        if(preyCells):
            predatorReproduction(times, cells, action, preyCells, y, x)
        elif(newStep): #si me muevo sin consumir
            predatorMovement(times, cells, action, newStep, y, x)
        else:
            pygame.draw.polygon(screen, RED, getRectangle(y, x), 0)


def predadorBehaviour(times, cells, action, y, x):
    if(times[y][x] <= 0): #si ha muerto
        cells[y][x] = NOTHING
        times[y][x] = 0
    else: #Movimiento y reproduccion de un depredador
        predatorRules(times, cells, action, y, x)

# ------------------------------------------------------------------------
# Simulation management methods
# ------------------------------------------------------------------------
    
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
                    elif((not (TYPEMASK & cells[y][x])) and (EMPTYMASK | cells[y][x] > 0)): #PREY 
                        preyBehaviour(times, cells, action, y, x)

            pygame.display.flip()

            if(np.sum(cells) != 0):
                times = times - 1 #resto 1 tiempo a todas las celulas
                action = np.ones([NY, NX], dtype="int")

def initializeSimulation(times, cells):
    pool = np.array([0, 1, 2])

    for y in range (0, NY):
        for x in range (0, NX):
            rectangle = getRectangle(y, x)
            choice = random.choice(pool)
            if(choice == 1): #PREDATOR #TODO GENERAR UN MENOR PORCENTAJE DE ELLOS
                cells[y][x], times[y][x] = PREDATOR, TIMEPREDATOR
                pygame.draw.polygon(screen, RED, (rectangle), 0)
            elif(choice == 2): #PREY
                cells[y][x], times[y][x] = PREY, TIMEPREY
                pygame.draw.polygon(screen, GREEN, (rectangle), 0)

    #cells[3][3], times[3][3] = PREDATOR, TIMEPREDATOR
    #pygame.draw.polygon(screen, RED, (getRectangle(3, 3)), 0)

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