class cell(object):
    def __init__(self, cellType, cellStatus, timeToRepro):
        self._cellType = cellType
        self._cellStatus = cellStatus
        self._timeAlive = 0
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

    def updateTimeAlive(self, time=1):
        self._timeAlive += time

    def updateTimeToRepro(self,time=-1):
        self._timeToRepro += time