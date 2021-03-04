import pygame
import numpy as np
import random
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
Y_PREDATOR = 0b1001
A_PREDATOR = 0b1010

Y_PREY = 0b0001
A_PREY = 0b0010

NOTHING = 0b0000

# Masks
# ------------------------------------------------------------------------
TYPEMASK = 0b1000
EMPTYMASK = 0b0000
YOUNGMASK = 0b0001
ADULTMASK = 0b0010

# ------------------------------------------------------------------------
# Cells generation and control
# ------------------------------------------------------------------------

# Generation
# ------------------------------------------------------------------------
PREY_PERCENTAGE = PREY_VALUE / 100
PREDATOR_PERCENTAGE = PREDATOR_VALUE / 100
PREYCELLS = (int) (NX * NY * PREY_PERCENTAGE)
PREDATORCELLS = (int) (NX * NY * PREDATOR_PERCENTAGE)

# Reproduction and growth values (this will be moved into another .py in the future when i implement the GUI)
# ------------------------------------------------------------------------
TIMEPREDATOR = 7
TIMEY_PREY = 9
TIMESIM = 0.3

PRE_REPRO_CONDITION = 3
PRE_REPRO_RATE = 2

PREY_VALUE = 27
PREDATOR_VALUE = 1

PREYGROWTHRATIO = 4
PREDATORGROWTHRATIO = 3

# ------------------------------------------------------------------------
# Neighbors position vectors
# ------------------------------------------------------------------------
NEIGHBORS = 8
NYCOORD = [1,  1,  1, -1, -1, -1, 0 ,  0]
NXCOORD = [1,  0, -1,  1,  0, -1, 1 , -1]