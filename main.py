#from constants import *
from prey import *
from predator import *
from empyCell import *
from preyBehaviour import *
from predatorBehaviour import *

# ------------------------------------------------------------------------
# Simulation management methods
# ------------------------------------------------------------------------
def runSimulation(times, cells, action):
    running = True
    paused = False

    preysAI = preyBehaviour()
    predatorsAI = predatorBehaviour()

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
                    if (cells[y][x].getCellType() == PREDATOR): #PREDATOR
                        predatorsAI.behaviour(times, cells, action, y, x) 
                    elif(cells[y][x].getCellType() == PREY):  #Y_PREY 
                        preysAI.behaviour(times, cells, action, y, x)
                    
            pygame.display.flip()   
            """for y in range (0, NY):
                for x in range (0, NX): 
                    if(cells[y][x].getCellType() == PREDATOR):
                        print(1, end= " ")
                    elif(cells[y][x].getCellType() == PREY):
                        print(2, end= " ")
                    else:
                        print(0, end= " ")
                print()"""

            action = np.ones([NY, NX], dtype="int")

def initializeSimulation(times, cells):
    #TODO: generar elmentos totalmente diferentes, hay veces que se pisan unos a otros
    preyCount, predatorCount = PREYCELLS, PREDATORCELLS
    for i in range(0, PREYCELLS + PREDATORCELLS):
        y = np.random.randint(1, NY)
        x = np.random.randint(1, NX)
        rectangle = getRectangle(y, x)
        if(predatorCount and cells[y][x].getCellType() == NONE):
            cells[y][x] = predator()
            pygame.draw.polygon(screen, RED_Y, rectangle, 0)
            predatorCount -= 1
        elif(preyCount and cells[y][x].getCellType() == NONE):
            cells[y][x] = prey()
            pygame.draw.polygon(screen, GREEN_Y, rectangle, 0)
            preyCount -= 1

    print(predatorCount, " ", preyCount)
    pygame.display.flip()

def main():
    pygame.display.set_caption("Cellular automata")
    clock = pygame.time.Clock()
    clock.tick(FPS)
    screen.fill(BLACK)

    row = [emptyCell() for i in range(NX)]
    cells = [list(row) for i in range(NY)]

    times = np.zeros([NY, NX], dtype="int")
    action = np.ones([NY, NX], dtype="int") #tengo que ver si cambiar esto o dejarlo así (habiendo pasado a OO no tiene mucho sentido)
    
    initializeSimulation(times, cells)
    runSimulation(times, cells, action)

                
if __name__ == "__main__":
    main()