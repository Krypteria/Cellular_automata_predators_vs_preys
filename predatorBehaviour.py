from constants import *
from generalMethods import getRectangle
from cell import predator, emptyCell 

# -----------------------------------------------------------------------------------------------------------#
# Rules                                                                                                      #
# -----------------------------------------------------------------------------------------------------------#

# Growth                                                                                                         
# -----------------------------------------------------------------------------------------------------------#   
# - If the time alive of a young predator is equal to YOUNG_PREDATOR_AGE_LIMIT it becomes an Adult predator. #   
# - If the time alive of an adult predator is equal to ADULT_PREDATOR_AGE_LIMIT it becomes an old predator.  #   
# - If the time alive of an old predator is equal to OLD_PREDATOR_AGE_LIMIT it dies.                         #   
# -----------------------------------------------------------------------------------------------------------#                                                                                                                       #

# Reproduction / eat                                                                                             
# -----------------------------------------------------------------------------------------------------------#   
# - Young predators don't have the ability to reproduce, but they can eat prey in adjacent cells by moving   #
#   to that cell.                                                                                            #
#                                                                                                            #   
# - Adult predator can reproduce if timeToReproduction is equal to 0 and:                                    #
#   - If there are PREDATOR_REPRODUCTION_CONDITION preys in the adjacent cells, then, the predator generate  #   
#     PREDATOR_REPRODUCTION_RATE young predators in those cells.                                             #   
#   - If the above condition is not met but there is at least one prey in the adjacent cells, then, the      #   
#     predator generate a new young predator cell in that position.                                          # 
#                                                                                                            # 
# - Old predators don't have the ability to reproduce, but they can eat prey in adjacent cells by moving     #
#   to that cell.                                                                                            #        
# -----------------------------------------------------------------------------------------------------------#  

# Movement                                                                                                       
# -----------------------------------------------------------------------------------------------------------#   
# - The predators only move when they cannot eat a prey cell or reproduce and have and empty cell in         #
#   adjacent cells.                                                                                          #   
# - Old ones have a 50% chance to not move and stay in the same spot.                                        #   
# -----------------------------------------------------------------------------------------------------------#   
                                                                                                                   
# -----------------------------------------------------------------------------------------------------------#
# -----------------------------------------------------------------------------------------------------------#

class predatorBehaviour(object):

    # Public methods
    # ------------------------------------------------------------------------

    def behaviour(self, cells, action, y, x):
        if(action[y][x]):
            self.__growth(cells, y, x)
            cellStatus = cells[y][x].getCellStatus()

            if(cellStatus == YOUNG):
                self.__youngBehaviour(cells, action, y, x)
            elif(cellStatus == ADULT):
                self.__adultBehaviour(cells, action, y, x)
            elif(cellStatus == OLD):
                self.__oldBehaviour(cells, action, y, x)

    # Specific behaviour
    # ------------------------------------------------------------------------

    def __oldBehaviour(self, cells, action, y, x):
        newStep, preyCells = self.__newStepSearch(cells, y, x)
        if(preyCells):
            newY, newX = self.__eat(cells, action, preyCells, OLD, y, x)
            cells[newY][newX].updateTimes()
        elif(newStep and random.choice([1,0])):
            newY, newX = self.__movement(cells, action, newStep, OLD, y, x)
            cells[newY][newX].updateTimes()
        else:
            cells[y][x].updateTimes()
            pygame.draw.polygon(SCREEN, RED_OLD, getRectangle(y, x), 0)

    def __adultBehaviour(self, cells, action, y, x):
        newStep, preyCells = self.__newStepSearch(cells, y, x)
        if(preyCells and cells[y][x].getTimeToReproduction() <= 0):
            self.__reproduction(cells, action, preyCells, y, x)
            cells[y][x].updateTimes()
        elif(newStep):
            newY, newX = self.__movement(cells, action, newStep, ADULT, y, x)
            cells[newY][newX].updateTimes()
        else:
            cells[y][x].updateTimes()
            pygame.draw.polygon(SCREEN, RED_ADULT, getRectangle(y, x), 0)

    def __youngBehaviour(self,cells, action, y, x):
        newStep, preyCells = self.__newStepSearch(cells, y, x)
        if(preyCells):
            newY, newX = self.__eat(cells, action, preyCells, YOUNG, y, x)
            cells[newY][newX].updateTimes()
        elif(newStep):
            newY, newX = self.__movement(cells, action, newStep, YOUNG, y, x)
            cells[newY][newX].updateTimes()
        else:
            cells[y][x].updateTimes()
            pygame.draw.polygon(SCREEN, RED_YOUNG, getRectangle(y, x), 0)

    # General actions
    # ------------------------------------------------------------------------

    def __growth(self, cells, y, x):
        cellStatus, cellTime = cells[y][x].getCellStatus(), cells[y][x].getTimeAlive()
        if(cellStatus == YOUNG and cellTime == YOUNG_PREDATOR_AGE_LIMIT):
            cells[y][x].setCellStatus(ADULT)
        elif(cellStatus == ADULT and cellTime == ADULT_PREDATOR_AGE_LIMIT):
             cells[y][x].setCellStatus(OLD)
        elif((cellStatus == OLD) and cellTime == OLD_PREDATOR_AGE_LIMIT):
            cells[y][x] = emptyCell()
 
    def __eat(self, cells, action, preyCells, predatorStatus, y, x):
        newY, newX = random.choice(preyCells)
        cells[newY][newX] = predator(predatorStatus, cells[y][x].getTimeToReproduction(), cells[y][x].getTimeAlive())
        cells[y][x] = emptyCell()
        action[newY][newX] = 0

        if(predatorStatus == YOUNG):
            pygame.draw.polygon(SCREEN, RED_YOUNG, getRectangle(newY, newX))
        elif(predatorStatus == OLD):
            pygame.draw.polygon(SCREEN, RED_OLD, getRectangle(newY, newX))
        
        return newY, newX
        
    def __reproduction(self, cells, action, preyCells, y, x):
        k = PREDATOR_REPRODUCTION_RATE if len(preyCells) >= PREDATOR_REPRODUCTION_CONDITION else 1
        for i in range(0, k):
            newY, newX = random.choice(preyCells)
            preyCells.remove([newY, newX])
            cells[newY][newX] = predator()
            action[newY][newX] = 0
            pygame.draw.polygon(SCREEN, RED_YOUNG, getRectangle(newY, newX))
        action[y][x] = 0
        cells[y][x].updateTimeToRepro(TIME_UNTIL_REPRODUCTION_PREDATOR)
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
        elif(predatorStatus == OLD):
            pygame.draw.polygon(SCREEN, RED_OLD, getRectangle(newY, newX))
        
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