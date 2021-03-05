from constants import *
from cell import * 

class prey(cell):
    def __init__(self, cellStatus=YOUNG, timeToRepro=TIMEPREY): #AÑADIR TIMEALIVE CUANDO LO META
        cell.__init__(self, PREY, cellStatus, timeToRepro)