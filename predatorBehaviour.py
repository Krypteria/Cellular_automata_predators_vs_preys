from constants import *
from generalMethods import *
from empyCell import *
from predator import *

class predatorBehaviour(object):

    # Public methods
    # ------------------------------------------------------------------------

    def behaviour(self, times, cells, action, y, x):
        if(action[y][x]):
            self.__growth(times, cells, y, x)
            if(cells[y][x].getTimeToReproduction() == 0): #CAMBIAR CUANDO TIMEALIVE
                cells[y][x] = emptyCell()
            elif(cells[y][x].getCellStatus() == YOUNG):
                self.__youngBehaviour(times, cells, action, y, x)
            elif(cells[y][x].getCellStatus() == ADULT):
                self.__adultBehaviour(times, cells, action, y, x)

    # Private methods
    # ------------------------------------------------------------------------

    def __adultBehaviour(self, times, cells, action, y, x):
        preyCells = self.__foodSearch(cells, y, x)
        if(preyCells):
            self.__reproduction(times, cells, action, preyCells, y, x)
            cells[y][x].updateTimeToRepro()
        else:
            newStep = self.__newStepSearch(cells, y, x)
            if(newStep):
                newY, newX = self.__movement(times, cells, action, newStep, ADULT, y, x)
                cells[newY][newX].updateTimeToRepro()
            else:
                cells[y][x].updateTimeToRepro()
                pygame.draw.polygon(screen, RED_A, getRectangle(y, x), 0)


    def __youngBehaviour(self, times, cells, action, y, x):
        newStep = self.__newStepSearch(cells, y, x)
        if(newStep):
            newY, newX = self.__movement(times, cells, action, newStep, YOUNG, y, x)
            cells[newY][newX].updateTimeToRepro() 
        else:
            pygame.draw.polygon(screen, RED_Y, getRectangle(y, x), 0)

    # ------------------------------------------------------------------------

    def __growth(self, times, cells, y, x): 
        if((cells[y][x].getCellStatus() == YOUNG) and cells[y][x].getTimeToReproduction() < PREDATORGROWTHRATIO): #CAMBIAR CUANDO TIMEALIVE
            cells[y][x].setCellStatus(ADULT)
            pygame.draw.polygon(screen, RED_A, getRectangle(y, x), 0)

    #Coger el tiempo de la celula comida e ir sumando el tiempo para al final sumarselo a la celula de turno -> multiplica por PREYLIVESTEAL
    def __reproduction(self, times, cells, action, preyCells, y, x): 
        k = 1
        if(len(preyCells) >= PRE_REPRO_CONDITION):
            k = PRE_REPRO_RATE
        for i in range(0, k):
            newY, newX = random.choice(preyCells)
            preyCells.remove([newY, newX])
            cells[newY][newX] = predator()
            action[newY][newX] = 0
            draw(getRectangle(y, x), getRectangle(newY, newX), RED_A, RED_Y)  

        action[y][x] = 0

    def __movement(self, times, cells, action, newStep, predatorStatus, y, x):
        newY, newX = random.choice(newStep)
        cells[newY][newX] = predator(predatorStatus, cells[y][x].getTimeToReproduction())
        cells[y][x] = emptyCell()
        action[newY][newX] = 0
        if(predatorStatus == YOUNG):
            draw(getRectangle(y, x), getRectangle(newY, newX), BLACK, RED_Y)
        elif(predatorStatus == ADULT):
            draw(getRectangle(y, x), getRectangle(newY, newX), BLACK, RED_A)
        
        return newY, newX

    def __newStepSearch(self, cells, y, x):
        newStep = []
        for k in range (0, NEIGHBORS):
            newX = (x + NXCOORD[k]) % NX
            newY = (y + NYCOORD[k]) % NY
            if(cells[newY][newX].getCellStatus() == NONE):
                newStep.append([newY, newX])
        return newStep

    def __foodSearch(self, cells, y, x):
        preyCells = []
        for k in range(0, NEIGHBORS):
            newX = (x + NXCOORD[k]) % NX
            newY = (y + NYCOORD[k]) % NY
            if(cells[newY][newX].getCellType() == PREY): 
                preyCells.append([newY, newX])
        return preyCells