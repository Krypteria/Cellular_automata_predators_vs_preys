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

NY = 60
NX = 90

#CODIFICACIONES 
PREDATOR = 0b1010 
PREY = 0b0010
NOTHING = 0b0000

TIMEPREDATOR = 2
TIMEPREY = 1
TIMESIM = 1

#MASCARAS
TYPEMASK = 0b1000
EMPTYMASK = 0b0000

FPS = 60

screen = pygame.display.set_mode([HEIGHT, WIDTH])

#Vectores de posicion
pos = 8
Vf = [1,  1,  1, -1, -1, -1, 0 ,  0]
Vc = [1,  0, -1,  1,  0, -1, 1 , -1]

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

#TODO optimizar el calculo cuando todos los bloques estan ocupados por PREY
def preyRules(times, cells, turno, y, x):
    movimiento, reproduccion= False, False
    if(turno[y][x]):
        for k in range (0, pos):
            newX = (x + Vf[k]) % NX
            newY = (y + Vc[k]) % NY
            if(cells[newY][newX] == NOTHING):
                if(times[y][x] == 0): #se reproduce
                    cells[newY][newX], times[newY][newX] = PREY, TIMEPREY
                    times[y][x] = TIMEPREY
                    draw(getRectangle(y, x), getRectangle(newY, newX), GREEN, GREEN)
                    turno[y][x], turno[newY][newX] = 0, 0
                    reproduccion = True
                else: #movimiento
                    cells[newY][newX], times[newY][newX] = PREY, times[y][x]
                    cells[y][x], times[y][x] = NOTHING, 0
                    draw(getRectangle(y, x), getRectangle(newY, newX), BLACK, GREEN)
                    turno[newY][newX] = 0
                    movimiento = True
                break
        if(not movimiento and not reproduccion):
            pygame.draw.polygon(screen, GREEN, getRectangle(y, x), 0)
    

def preyBehaviour(times, cells, turno, y, x):
    preyRules(times, cells, turno, y, x)

# ------------------------------------------------------------------------
# Predator methods
# ------------------------------------------------------------------------

def predatorRules(times, cells, turno, y, x):
    freeX, freeY = -1, -1
    movimiento, reproduccion = False, False
    if(turno[y][x]):
        for k in range (0, pos):
            newX = (x + Vf[k]) % NX
            newY = (y + Vc[k]) % NY
            if(cells[newY][newX] == PREY): #si ataco a una presa me multiplico
                cells[newY][newX], times[newY][newX]  = PREDATOR, TIMEPREDATOR 
                draw(getRectangle(y, x), getRectangle(newY, newX), RED, RED)
                turno[y][x], turno[newY][newX] = 0, 0
                reproduccion = True 
                break
            elif(cells[newY][newX] == NOTHING):
                freeX, freeY = newX, newY
                movimiento = True

        if(not reproduccion and movimiento): #si me muevo sin consumir
            cells[freeY][freeX], times[freeY][freeX] = PREDATOR, times[y][x] #conservo el tiempo
            cells[y][x], times[y][x] = NOTHING, 0
            turno[freeY][freeX] = 0
            draw(getRectangle(y, x), getRectangle(freeY, freeX), BLACK, RED)

def predadorBehaviour(times, cells, turno, y, x):
    if(times[y][x] <= 0): #si ha muerto
        cells[y][x] = NOTHING
        times[y][x] = 0
    else: #Movimiento y reproduccion de un depredador
        predatorRules(times, cells, turno, y, x)

# ------------------------------------------------------------------------
# Simulation management methods
# ------------------------------------------------------------------------

def runSimulation(times, cells, turno):
    running = True
    paused = False
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                paused = not paused
        
        if(not paused):
            print("turno")
            screen.fill(BLACK)
            time.sleep(TIMESIM)
        
            for y in range (0, NY):
                for x in range (0, NX):
                    #Comprobamos que tipo de celula es
                    if (TYPEMASK & cells[y][x]): #PREDATOR
                        predadorBehaviour(times, cells, turno, y, x)
                    elif((not (TYPEMASK & cells[y][x])) and (EMPTYMASK | cells[y][x] > 0)): #PREY 
                        preyBehaviour(times, cells, turno, y, x)

            pygame.display.flip() 

            if(np.sum(cells) != 0):
                times = times - 1 #resto 1 tiempo a todas las celulas
                turno = np.ones([NY, NX], dtype="int")
           

                        #PREY -> si puede reproducirse hacemos una cosa, si no hacemos otra
                        #PREDATOR -> movimiento
                        #Nada -> siguiente

                        #El prey buscará una casilla vacia, el PREDATOR una que tenga un PREY o esté vacia

                    #Obtenemos información de los vecinos
                    #Realizamos movimiento / muerte / Reproducción (Rules)
                    #Comprobamos si hay un cambio de edad       
                    #Actualizamos edad y tiempo de fase
                    #lo repintamos
                    #TODO HACER MAS ALEATORIA LA ELECCION DE NUEVA CELDA

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
    pygame.display.flip()

def main():
    pygame.display.set_caption("Cellular automata")
    clock = pygame.time.Clock()
    clock.tick(FPS)
    screen.fill(BLACK)

    cells = np.zeros([NY, NX], dtype="int")
    times = np.zeros([NY, NX], dtype="int")
    turno = np.ones([NY, NX], dtype="int")
    
    initializeSimulation(times, cells)
    runSimulation(times, cells, turno)

                
if __name__ == "__main__":
    main()