from constants import *
from generalMethods import getRectangle
from cell import predator, prey, emptyCell
from preyBehaviour import preyBehaviour
from predatorBehaviour import predatorBehaviour

# ------------------------------------------------------------------------
# Simulation management methods
# ------------------------------------------------------------------------
def runSimulation(cells, action):
    running = True
    paused = False

    preysAI = preyBehaviour()
    predatorsAI = predatorBehaviour()

    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if(event.key is not pygame.K_r):
                    paused = not paused
                else:
                    cells = initializeSimulation()
                    if paused == True:
                        paused = False
        
        if(not paused):
            SCREEN.fill(BLACK)
            time.sleep(TIMESIM)       

            for y in range (0, NY):
                for x in range (0, NX):
                    if (cells[y][x].getCellType() == PREDATOR):
                        predatorsAI.behaviour(cells, action, y, x) 
                    elif(cells[y][x].getCellType() == PREY):
                        preysAI.behaviour(cells, action, y, x)     

            pygame.display.flip()   
            action = np.ones([NY, NX], dtype="int")

def initializeSimulation():
    row = [emptyCell() for i in range(NX)]
    cells = [list(row) for i in range(NY)]
    
    for i in range(PREDATOR_CELLS):
        y, x = np.random.randint(1, NY), np.random.randint(1, NX)
        if(cells[y][x].getCellType() == NONE):
            cells[y][x] = predator()
            pygame.draw.polygon(SCREEN, RED_YOUNG, getRectangle(y, x), 0)
    for i in range(PREY_CELLS):
        y, x = np.random.randint(1, NY), np.random.randint(1, NX)
        if(cells[y][x].getCellType() == NONE):
            cells[y][x] = prey()
            pygame.draw.polygon(SCREEN, GREEN_YOUNG, getRectangle(y, x), 0)
    pygame.display.flip()

    return cells


def main():
    pygame.display.set_caption("Prey vs predator simulation")
    clock = pygame.time.Clock()
    clock.tick(FPS)

    action = np.ones([NY, NX], dtype="int")
    
    cells = initializeSimulation()
    runSimulation(cells, action)

                
if __name__ == "__main__":
    main()