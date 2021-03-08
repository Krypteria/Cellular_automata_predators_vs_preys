from cell import *
from preyBehaviour import *
from predatorBehaviour import *

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
                paused = not paused
        
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

def initializeSimulation(cells):
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


def main():
    pygame.display.set_caption("Cellular automata: prey vs predator simulation")
    clock = pygame.time.Clock()
    clock.tick(FPS)

    row = [emptyCell() for i in range(NX)]
    cells = [list(row) for i in range(NY)]

    action = np.ones([NY, NX], dtype="int")
    
    initializeSimulation(cells)
    runSimulation(cells, action)

                
if __name__ == "__main__":
    main()