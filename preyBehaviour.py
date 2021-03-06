from constants import *
from generalMethods import *
from cell import prey, emptyCell


class preyBehaviour(object):

    # Public methods
    # ------------------------------------------------------------------------ 

    def behaviour(self, cells, action, y, x):
        if(action[y][x]): 
            self.__growth(cells, y, x)
            if(cells[y][x].getCellStatus() == YOUNG):
                self.__youngBehaviour(cells, action, y, x)
            elif(cells[y][x].getCellStatus() == ADULT):
                self.__adultBehaviour(cells, action, y, x)

    # Private methods
    # ------------------------------------------------------------------------ 

    def __adultBehaviour(self, cells, action, y, x):
        newStep = self.__newStepSearch(cells, y, x)
        if(newStep):
            if(cells[y][x].getTimeToReproduction() <= 0): 
                self.__reproduction(cells, action, newStep, y, x) 
                cells[y][x].updateTimes()
            elif(newStep):
                newY, newX = self.__movement(cells, action, newStep, ADULT, y, x)
                cells[newY][newX].updateTimes()
        else:
            cells[y][x].updateTimes()
            pygame.draw.polygon(SCREEN, GREEN_ADULT, getRectangle(y, x), 0)

    def __youngBehaviour(self, cells, action, y, x):
        newStep = self.__newStepSearch(cells, y, x)
        if(newStep):
            newY, newX = self.__movement(cells, action, newStep, YOUNG, y, x)
            cells[newY][newX].updateTimes()
        else:
            cells[y][x].updateTimes()
            pygame.draw.polygon(SCREEN, GREEN_YOUNG, getRectangle(y, x), 0)

    # ------------------------------------------------------------------------

    def __growth(self, cells, y, x):
        if((cells[y][x].getCellStatus() == YOUNG) and cells[y][x].getTimeAlive() >= YOUNG_PREY_LIMIT):
            cells[y][x].setCellStatus(ADULT)
            pygame.draw.polygon(SCREEN, GREEN_ADULT, getRectangle(y, x), 0)

    def __reproduction(self, cells, action, newStep, y, x):
        newY, newX = random.choice(newStep)
        newStep.remove([newY, newX])
        cells[newY][newX] = prey()
        cells[y][x].updateTimeToRepro(TIMEPREY)
        action[y][x], action[newY][newX] = 0, 0

        pygame.draw.polygon(SCREEN, GREEN_ADULT, getRectangle(y, x), 0)
        pygame.draw.polygon(SCREEN, GREEN_YOUNG, getRectangle(newY, newX), 0)
        return newStep

    def __movement(self, cells, action, newStep, preyStatus, y, x):
        newY, newX = random.choice(newStep)
        cells[newY][newX] = prey(preyStatus, cells[y][x].getTimeToReproduction(), cells[y][x].getTimeAlive()) 
        cells[y][x] = emptyCell()
        action[newY][newX] = 0

        if(preyStatus == YOUNG):
            pygame.draw.polygon(SCREEN, GREEN_YOUNG, getRectangle(newY, newX), 0)
        elif(preyStatus == ADULT):
            pygame.draw.polygon(SCREEN, GREEN_ADULT, getRectangle(newY, newX), 0)
        
        return newY, newX

    def __newStepSearch(self, cells, y, x):
        newStep = []
        for k in range (0, NEIGHBORS): 
            newX = (x + NX_COORD[k]) % NX
            newY = (y + NY_COORD[k]) % NY
            if(cells[newY][newX].getCellType() == NONE):
                newStep.append([newY, newX])
        return newStep
