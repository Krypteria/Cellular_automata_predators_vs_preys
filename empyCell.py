from cell import *
from constants import *

class emptyCell(cell):
    def __init__(self):
        cell.__init__(self, NONE, NONE, 0, 0)