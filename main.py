from constants import *
from prey import *
from predator import *


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