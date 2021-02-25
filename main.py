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

TIMEPREDATOR = 4
TIMEPREY = 18

#MASCARAS
TYPEMASK = 0b1000
EMPTYMASK = 0b0000

FPS = 60

#Vectores de posicion
pos = 8
Vf = [1,  1,  1, -1, -1, -1, 0 ,  0]
Vc = [1,  0, -1,  1,  0, -1, 1 , -1]



def getRectangle(x, y):
    return [(x * RW, y * RH), ((x + 1) * RW, y * RH), ((x + 1) * RW, (y + 1)* RH), (x * RW, (y + 1) * RH)]

def predadorRules(screen, times, cells, x, y):
    if(times[x][y] <= 0): #si ha muerto
        cells[x][y] = NOTHING
        times[x][y] = 0
        rectangle = getRectangle(x, y)
        pygame.draw.polygon(screen, BLACK, (rectangle), 0)
    else: #Movimiento y reproduccion de un depredador
        freeX = -1
        freeY = -1
        for k in range (0, pos):
            nX = x + Vf[k]
            nY = y + Vc[k]
            if(cells[nX][nY] == PREY): #si ataco a una presa me multiplico
                cells[nX][nY] = PREDATOR
                times[nX][nY] = TIMEPREDATOR
                rectangle = getRectangle(nX, nY)
                pygame.draw.polygon(screen, RED, (rectangle), 0)
                freeX = -1 
                freeY = -1
                break
            elif(cells[nX][nY] == NOTHING):
                freeX = nX
                freeY = nY
        if(freeX != -1 and freeY != -1): #si me muevo sin consumir
            cells[freeX][freeY] = PREDATOR
            times[freeX][freeY] = times[x][y] #conservo el tiempo
            rectangle = getRectangle(freeX, freeY)
            pygame.draw.polygon(screen, RED, (rectangle), 0)


def initializeSimulation(screen, times, cells):
    #Inicialización de la matriz
    pool = np.array([0, 1, 2])
 
    for x in range (0, NX):
        for y in range (0, NY):
            rectangle = getRectangle(x, y)
            choice = random.choice(pool)

            if(choice == 1 and x == 2): #PREDATOR
                cells[x][y] = PREDATOR
                times[x][y] = TIMEPREDATOR
                pygame.draw.polygon(screen, RED, (rectangle), 0)
            elif(choice == 2): #PREY
                cells[x][y] = PREY
                times[x][y] = TIMEPREY
                pygame.draw.polygon(screen, GREEN, (rectangle), 0)
    print(cells)
    pygame.display.flip()

def runSimulation(screen, times, cells):
    running = True
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #Turno
        print("turno")
        time.sleep(0.3)
        screen.fill(BLACK)
        times = times - 1 #resto 1 tiempo a todas las celulas
        for x in range (0, NX -1):
            for y in range (0, NY -1):
                #Comprobamos que tipo de celula es
                if (TYPEMASK & cells[x][y]): #PREDATOR
                    predadorRules(screen, times, cells, x, y)
                elif(EMPTYMASK | cells[x][y]): #PREY 
                    Rectangle = getRectangle(x, y)
                    pygame.draw.polygon(screen, GREEN, (Rectangle), 0)

                
                    #PREY -> si puede reproducirse hacemos una cosa, si no hacemos otra
                    #PREDATOR -> movimiento
                    #Nada -> siguiente

                    #El prey buscará una casilla vacia, el PREDATOR una que tenga un PREY o esté vacia

                #Obtenemos información de los vecinos
                #Realizamos movimiento / muerte / Reproducción (Rules)
                #Comprobamos si hay un cambio de edad       
                #Actualizamos edad y tiempo de fase
                #lo repintamos
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