from constants import *
from generalMethods import *
from cell import predator, emptyCell 

class predatorBehaviour(object):

    # Public methods
    # ------------------------------------------------------------------------

    def behaviour(self, cells, action, y, x):
        if(action[y][x]):
            self.__growth(cells, y, x)
            if(cells[y][x].getTimeAlive() >= DIE_PREDATOR_LIMIT):
                cells[y][x] = emptyCell()
            elif(cells[y][x].getCellStatus() == YOUNG):
                self.__youngBehaviour(cells, action, y, x)
            elif(cells[y][x].getCellStatus() == ADULT):
                self.__adultBehaviour(cells, action, y, x)

    # Private methods
    # ------------------------------------------------------------------------

    def __adultBehaviour(self, cells, action, y, x):
        newStep, preyCells = self.__newStepSearch(cells, y, x)
        if(preyCells):
            self.__reproduction(cells, action, preyCells, y, x)
            cells[y][x].updateTimes()
        elif(newStep):
            newY, newX = self.__movement(cells, action, newStep, ADULT, y, x)
            cells[newY][newX].updateTimes()
        else:
            cells[y][x].updateTimes()
            pygame.draw.polygon(SCREEN, RED_ADULT, getRectangle(y, x), 0)

    def __youngBehaviour(self,cells, action, y, x):
        newStep = self.__newStepSearch(cells, y, x)[0]
        if(newStep):
            newY, newX = self.__movement(cells, action, newStep, YOUNG, y, x)
            cells[newY][newX].updateTimes()
        else:
            cells[y][x].updateTimes()
            pygame.draw.polygon(SCREEN, RED_YOUNG, getRectangle(y, x), 0)

    # ------------------------------------------------------------------------

    def __growth(self, cells, y, x): 
        if((cells[y][x].getCellStatus() == YOUNG) and cells[y][x].getTimeAlive() >= YOUNG_PREDATOR_LIMIT):
            cells[y][x].setCellStatus(ADULT)
            pygame.draw.polygon(SCREEN, RED_ADULT, getRectangle(y, x), 0)
 
    def __reproduction(self, cells, action, preyCells, y, x):
        k = PRE_REPRO_CONDITION if len(preyCells) >= PRE_REPRO_CONDITION else 1
        for i in range(0, k):
            newY, newX = random.choice(preyCells)
            preyCells.remove([newY, newX])
            cells[newY][newX] = predator()
            action[newY][newX] = 0
            pygame.draw.polygon(SCREEN, RED_YOUNG, getRectangle(newY, newX))

        action[y][x] = 0
        pygame.draw.polygon(SCREEN, RED_ADULT, getRectangle(y, x))

    def __movement(self, cells, action, newStep, predatorStatus, y, x):
        newY, newX = random.choice(newStep)
        cells[newY][newX] = predator(predatorStatus, cells[y][x].getTimeToReproduction(), cells[y][x].getTimeAlive())
        cells[y][x] = emptyCell()
        action[newY][newX] = 0

        if(predatorStatus == YOUNG):
            pygame.draw.polygon(SCREEN, RED_YOUNG, getRectangle(newY, newX))
        elif(predatorStatus == ADULT):
            pygame.draw.polygon(SCREEN, RED_ADULT, getRectangle(newY, newX))
        
        return newY, newX

    def __newStepSearch(self, cells, y, x):
        newStep, preyCells = [], []

        for k in range (0, NEIGHBORS):
            newX = (x + NX_COORD[k]) % NX
            newY = (y + NY_COORD[k]) % NY

            cellType = cells[newY][newX].getCellType() 
            if(cellType == NONE):
                newStep.append([newY, newX])
            elif(cellType == PREY): 
                preyCells.append([newY, newX])

        return newStep, preyCells