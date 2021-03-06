class cell(object):
    def __init__(self, cellType, cellStatus, timeToRepro, timeAlive):
        self._cellType = cellType
        self._cellStatus = cellStatus
        self._timeAlive = timeAlive
        self._timeToRepro = timeToRepro
    
    def getCellType(self):
        return self._cellType

    def getCellStatus(self):
        return self._cellStatus

    def getTimeAlive(self):
        return self._timeAlive
    
    def getTimeToReproduction(self):
        return self._timeToRepro

    def setCellType(self, newType):
        self._cellType = newType

    def setCellStatus(self, newStatus):
        self._cellStatus = newStatus

    def updateTimes(self):
        self._timeToRepro -= 1
        self._timeAlive +=1

    def updateTimeToRepro(self, newValue):
        self._timeToRepro = newValue