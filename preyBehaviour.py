from constants import *
from generalMethods import *
from prey import *
from empyCell import *


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

    def __adultBehaviour(self, cells, action, y, x): #PROBLEMA CON EL TIEMPO DE REPRODUCCION, no podemos actualizar y,x ya que la celula puede estar en ny, nx
        newStep = self.__newStepSearch(cells, y, x)
        move = False
        if(newStep):
            if(cells[y][x].getTimeToReproduction() <= 0): 
                newStep = self.__reproduction(cells, action, newStep, y, x) 
            if(newStep):
                newY, newX = self.__movement(cells, action, newStep, ADULT, y, x)
                move = True
                
            if(move):
                cells[newY][newX].updateTimeToRepro()
            else:
                cells[y][x].updateTimeToRepro()
        else:
            cells[y][x].updateTimeToRepro()
            pygame.draw.polygon(screen, GREEN_A, getRectangle(y, x), 0)

    def __youngBehaviour(self, cells, action, y, x):
        newStep = self.__newStepSearch(cells, y, x)
        if(newStep):
            newY, newX = self.__movement(cells, action, newStep, YOUNG, y, x)
            cells[newY][newX].updateTimeToRepro()
        else:
            cells[y][x].updateTimeToRepro()
            pygame.draw.polygon(screen, GREEN_Y, getRectangle(y, x), 0)

    # ------------------------------------------------------------------------

    def __growth(self, cells, y, x):
        if((cells[y][x].getCellStatus() == YOUNG) and cells[y][x].getTimeToReproduction() < PREYGROWTHRATIO): #CAMBIAR CUANDO TIMEALIVE
            cells[y][x].setCellStatus(ADULT)
            pygame.draw.polygon(screen, GREEN_A, getRectangle(y, x), 0)

    def __reproduction(self, cells, action, newStep, y, x):
        newY, newX = random.choice(newStep)
        newStep.remove([newY, newX])

        cells[newY][newX] = prey()
        cells[y][x].updateTimeToRepro(TIMEPREY)
        action[y][x], action[newY][newX] = 0, 0
        draw(getRectangle(y, x), getRectangle(newY, newX), GREEN_A, GREEN_Y)
        return newStep

    def __movement(self, cells, action, newStep, preyStatus, y, x):
        newY, newX = random.choice(newStep)

        cells[newY][newX] = prey(preyStatus, cells[y][x].getTimeToReproduction()) 
        cells[y][x] = emptyCell()
        action[newY][newX] = 0

        if(preyStatus == YOUNG):
            pygame.draw.polygon(screen, GREEN_Y, getRectangle(newY, newX), 0)
        elif(preyStatus == ADULT):
            pygame.draw.polygon(screen, GREEN_A, getRectangle(newY, newX), 0)
        
        return newY, newX

        

    def __newStepSearch(self, cells, y, x):
        newStep = []
        for k in range (0, NEIGHBORS): #cambiar por comprehension list
            newX = (x + NXCOORD[k]) % NX
            newY = (y + NYCOORD[k]) % NY
            if(cells[newY][newX].getCellType() == NONE):
                newStep.append([newY, newX])
        return newStep
