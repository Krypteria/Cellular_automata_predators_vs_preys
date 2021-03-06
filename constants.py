import pygame
import random
import time
import numpy as np
pygame.font.init()

# ------------------------------------------------------------------------
# Screen and drawing
# ------------------------------------------------------------------------

# Screen constants
# ------------------------------------------------------------------------
HEIGHT, WIDTH  = 600, 900
RW, RH = 10, 10
NY, NX = (int) (HEIGHT / RH), (int) (WIDTH / RW)

SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])
FPS = 60

# Custom colors
# ------------------------------------------------------------------------
GRAY = (125,125,125)
BLACK = (0, 0, 0)
WHITE = (255,255,255)

RED_ADULT = (200,30,30) 
RED_YOUNG = (255,51,135) 

GREEN_YOUNG = (0,255,1)
GREEN_ADULT = (19,126,19)
#GREEN_OLD = (12,50,14)

# ------------------------------------------------------------------------
# Encodings
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
PREY_CELLS = (int) (NX * NY * PREY_PERCENTAGE)
PREDATOR_CELLS = (int) (NX * NY * PREDATOR_PERCENTAGE)

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

# ------------------------------------------------------------------------
# Neighbors position vectors
# ------------------------------------------------------------------------
NEIGHBORS = 8
NY_COORD = [1,  1,  1, -1, -1, -1, 0 ,  0]
NX_COORD = [1,  0, -1,  1,  0, -1, 1 , -1]