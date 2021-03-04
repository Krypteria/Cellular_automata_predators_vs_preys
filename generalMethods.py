from constants import *

# ------------------------------------------------------------------------
# General methods
# ------------------------------------------------------------------------

def getRectangle(y, x):
    return [(x * RW, y * RH), ((x + 1) * RW, y * RH), ((x + 1) * RW, (y + 1)* RH), (x * RW, (y + 1) * RH)]

def draw(source, nextStep, colorA, colorB):
    pygame.draw.polygon(screen, colorA, source, 0)
    pygame.draw.polygon(screen, colorB, nextStep, 0)