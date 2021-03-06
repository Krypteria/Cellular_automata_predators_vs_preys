from constants import *
from cell import * 

class predator(cell):
    def __init__(self, cellStatus=YOUNG, timeToRepro=TIMEPREDATOR, timeAlive=0):
        cell.__init__(self, PREDATOR, cellStatus, timeToRepro, timeAlive)