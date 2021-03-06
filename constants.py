import pygame
import numpy as np
import random
from itertools import combinations
import time
pygame.font.init()

# ------------------------------------------------------------------------
# Screen and drawing
# ------------------------------------------------------------------------

# Screen constants
# ------------------------------------------------------------------------
HEIGHT, WIDTH  = 600, 900
RW, RH = 10, 10

NY, NX = (int) (HEIGHT / RH), (int) (WIDTH / RW)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
font = pygame.font.SysFont("arial", 20)
FPS = 60

# Custom colors
# ------------------------------------------------------------------------
GRAY = (125,125,125)
BLACK = (0, 0, 0)
WHITE = (255,255,255)

RED_A = (200,30,30) 
RED_Y = (255,51,135) 

GREEN_Y = (0,255,1)
GREEN_A = (19,126,19)
GREEN_O = (12,50,14)

# ------------------------------------------------------------------------
# Encodings and masks
# ------------------------------------------------------------------------

# Encoding
# ------------------------------------------------------------------------
PREDATOR = "predator"
PREY = "prey"
NONE = "none"

YOUNG = "young"
ADULT = "adult"
OLD = "old"

# ------------------------------------------------------------------------
# Cells generation and control
# ------------------------------------------------------------------------

# Generation
# ------------------------------------------------------------------------
PREY_VALUE = 27
PREDATOR_VALUE = 1

PREY_PERCENTAGE = PREY_VALUE / 100
PREDATOR_PERCENTAGE = PREDATOR_VALUE / 100
PREYCELLS = (int) (NX * NY * PREY_PERCENTAGE)
PREDATORCELLS = (int) (NX * NY * PREDATOR_PERCENTAGE)

# Reproduction and growth values (this will be moved into another .py in the future when i implement the GUI)
# ------------------------------------------------------------------------
TIMESIM = 0.3

#Reproduction
TIMEPREDATOR = 7
TIMEPREY = 9

PRE_REPRO_CONDITION = 3
PRE_REPRO_RATE = 2

#Growth
YOUNG_PREY_LIMIT = 4
YOUNG_PREDATOR_LIMIT = 3
DIE_PREY_LIMIT = 20
DIE_PREDATOR_LIMIT = 7

PREYGROWTHRATIO = 4
PREDATORGROWTHRATIO = 3

# ------------------------------------------------------------------------
# Neighbors position vectors
# ------------------------------------------------------------------------
NEIGHBORS = 8
NYCOORD = [1,  1,  1, -1, -1, -1, 0 ,  0]
NXCOORD = [1,  0, -1,  1,  0, -1, 1 , -1]