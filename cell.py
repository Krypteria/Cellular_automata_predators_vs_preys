from constants import *

class cell(object):
    def __init__(self, cellType, cellStatus, timeToRepro, timeAlive):
        self.__cellType = cellType
        self.__cellStatus = cellStatus
        self.__timeAlive = timeAlive
        self.__timeToReproduction = timeToRepro
    
    def getCellType(self):
        return self.__cellType

    def getCellStatus(self):
        return self.__cellStatus

    def getTimeAlive(self):
        return self.__timeAlive
    
    def getTimeToReproduction(self):
        return self.__timeToReproduction

    def setCellType(self, newType):
        self.__cellType = newType

    def setCellStatus(self, newStatus):
        self.__cellStatus = newStatus

    def updateTimes(self):
        if(self.__cellStatus == ADULT):
            self.__timeToReproduction -= 1
        self.__timeAlive +=1

    def updateTimeToRepro(self, newValue):
        self.__timeToReproduction = newValue

class prey(cell):
    def __init__(self, cellStatus=YOUNG, timeToReproduction=TIME_UNTIL_REPRODUCTION_PREY, timeAlive=0): 
        cell.__init__(self, PREY, cellStatus, timeToReproduction, timeAlive)
        
class predator(cell):
    def __init__(self, cellStatus=YOUNG, timeToReproduction=TIME_UNTIL_REPRODUCTION_PREDATOR, timeAlive=0):
        cell.__init__(self, PREDATOR, cellStatus, timeToReproduction, timeAlive)

class emptyCell(cell):
    def __init__(self):
        cell.__init__(self, NONE, NONE, 0, 0)