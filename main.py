import pygame
import numpy as np
import random
import time

HEIGHT = 900
WIDTH = 600
GRAY = (125,125,125)
BLACK = (0, 0, 0)
GREEN = (48,138,52)
RED = (200,30,30)

RW = 10
RH = 10

NX = 90
NY = 60

#CODIFICACIONES 
PREDATOR = 0b1010 
PREY = 0b0010
NOTHING = 0b0000

TIMEPREDATOR = 2.5
TIMEPREY = 1
TIMESIM = 0.2

#MASCARAS
TYPEMASK = 0b1000
EMPTYMASK = 0b0000

FPS = 60


#Vectores de posicion
pos = 8
Vf = [1,  1,  1, -1, -1, -1, 0 ,  0]
Vc = [1,  0, -1,  1,  0, -1, 1 , -1]

# ------------------------------------------------------------------------
# General methods
# ------------------------------------------------------------------------

def getRectangle(x, y):
    return [(x * RW, y * RH), ((x + 1) * RW, y * RH), ((x + 1) * RW, (y + 1)* RH), (x * RW, (y + 1) * RH)]

def draw(screen, source, nextStep, colorA, colorB):
    pygame.draw.polygon(screen, colorA, source, 0)
    pygame.draw.polygon(screen, colorB, nextStep, 0)

# ------------------------------------------------------------------------
# Prey methods
# ------------------------------------------------------------------------

#TODO optimizar el calculo cuando todos los bloques estan ocupados por PREY y mirar por que no se pinta como deberia pintarse todo
def preyRules(screen, times, cells, x, y):
    movimiento, reproduccion= False, False
    for k in range (0, pos):
        newX = (x + Vf[k]) % NX
        newY = (y + Vc[k]) % NY
        if(cells[newX][newY] == NOTHING):
            if(times[x][y] == 0): #se reproduce
                cells[newX][newY], times[newX][newY] = PREY, TIMEPREY
                times[x][y] = TIMEPREY
                draw(screen, getRectangle(x, y), getRectangle(newX, newY), GREEN, GREEN)
                reproduccion = True
            else: #movimiento
                cells[newX][newY], times[newX][newY] = PREY, times[x][y]
                cells[x][y], times[x][y] = NOTHING, 0
                draw(screen, getRectangle(x, y), getRectangle(newX, newY), BLACK, GREEN)
                movimiento = True
            break
    if(not movimiento and not reproduccion):
        pygame.draw.polygon(screen, GREEN, getRectangle(x, y), 0)

def preyBehaviour(screen, times, cells, x, y):
    preyRules(screen, times, cells, x, y)

# ------------------------------------------------------------------------
# Predator methods
# ------------------------------------------------------------------------

def predatorRules(screen, times, cells, x, y):
    freeX, freeY = -1, -1
    movimiento, reproduccion = False, False
    for k in range (0, pos):
        newX = (x + Vf[k]) % NX
        newY = (y + Vc[k]) % NY
        if(cells[newX][newY] == PREY): #si ataco a una presa me multiplico
            cells[newX][newY], times[newX][newY]  = PREDATOR, TIMEPREDATOR 
            draw(screen, getRectangle(x, y), getRectangle(newX, newY), RED, RED)
            reproduccion = True 
            break
        elif(cells[newX][newY] == NOTHING):
            freeX, freeY = newX, newY
            movimiento = True

    if(not reproduccion and movimiento): #si me muevo sin consumir
        cells[freeX][freeY], times[freeX][freeY] = PREDATOR, times[x][y] #conservo el tiempo
        cells[x][y], times[x][y] = NOTHING, 0
        draw(screen, getRectangle(x, y), getRectangle(freeX, freeY), BLACK, RED)

def predadorBehaviour(screen, times, cells, x, y):
    if(times[x][y] <= 0): #si ha muerto
        cells[x][y] = NOTHING
        times[x][y] = 0
    else: #Movimiento y reproduccion de un depredador
        predatorRules(screen, times, cells, x, y)

# ------------------------------------------------------------------------
# Simulation management methods
# ------------------------------------------------------------------------

def runSimulation(screen, times, cells):
    running = True
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        print("turno")
        screen.fill(BLACK)
        if(np.sum(cells) != 0):
            times = times - 1 #resto 1 tiempo a todas las celulas
        time.sleep(TIMESIM)
    
        for x in range (0, NX):
            for y in range (0, NY):
                #Comprobamos que tipo de celula es
                if (TYPEMASK & cells[x][y]): #PREDATOR
                    predadorBehaviour(screen, times, cells, x, y)
                elif(not (TYPEMASK & cells[x][y]) and (EMPTYMASK | cells[x][y])): #PREY 
                    preyBehaviour(screen, times, cells, x, y)
        pygame.display.flip()  
                    #PREY -> si puede reproducirse hacemos una cosa, si no hacemos otra
                    #PREDATOR -> movimiento
                    #Nada -> siguiente

                    #El prey buscará una casilla vacia, el PREDATOR una que tenga un PREY o esté vacia

                #Obtenemos información de los vecinos
                #Realizamos movimiento / muerte / Reproducción (Rules)
                #Comprobamos si hay un cambio de edad       
                #Actualizamos edad y tiempo de fase
                #lo repintamos

def initializeSimulation(screen, times, cells):
    pool = np.array([0, 1, 2])

    for x in range (0, NX):
        for y in range (0, NY):
            rectangle = getRectangle(x, y)
            choice = random.choice(pool)

            if(choice == 1 and x == 2): #PREDATOR
                cells[x][y], times[x][y] = PREDATOR, TIMEPREDATOR
                pygame.draw.polygon(screen, RED, (rectangle), 0)
            elif(choice == 2): #PREY
                cells[x][y], times[x][y] = PREY, TIMEPREY
                pygame.draw.polygon(screen, GREEN, (rectangle), 0)

    pygame.display.flip()

def main():
    pygame.display.set_caption("Cellular automata")
    clock = pygame.time.Clock()
    clock.tick(FPS)
    screen = pygame.display.set_mode([HEIGHT, WIDTH])
    screen.fill(BLACK)

    cells = np.zeros([NX, NY], dtype="int")
    times = np.zeros([NX, NY], dtype="int")

    initializeSimulation(screen, times, cells)
    runSimulation(screen, times, cells)

                
if __name__ == "__main__":
    main()