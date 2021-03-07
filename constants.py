import pygame
import random
import time
import numpy as np
pygame.font.init()

# ------------------------------------------------------------------------
# RULES
# ------------------------------------------------------------------------
"""
    Si tiempoAlive == YOUNG_LIMIT -> celula pasa a etapa madura
    Si tiempoAlive == ADULT_LIMIT -> celula pasa a etapa vieja
    si tiempoAlive == DIE_LIMIT -> celula pasa a muerta


    PREY ADULTO
        Si un tiempoRepro == 0 en un prey -> se reproduce creando una nueva celula joven 
    PREY JOVEN 
        Se mueve aleatoriamente
    PREY VIEJO
        probabilidad del 50% de moverse aleatoriamente

    PREDATOR ADULTO
        Si número de celulas prey vecinas >= PREDATOR_REPRO_CONDITION: 
         -el depredador se come PREDATOR_REPRO_RATIO celulas y crea en su lugar depredadores jovenes
        Si no se cumple esa condición pero hay al menos una celula prey vecina:
         -el depredador se come a esa celula y crea un nuevo depredador joven
    PREDATOR JOVEN
        - Si tiene una celula prey como vecina se la come moviendose a esa posicion
        - Si no tiene entonces se mueve aleatoriamente
    PREDATOR VIEJO
        - Si tiene una celula prey como vecina se la come moviendose a esa posicion
        - Si no tiene entonces se mueve con una probabilidad del 50% a una casilla aleatoria
"""

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

RED_ADULT = (255,0,0) 
RED_YOUNG = (159,0,0) 
RED_OLD = (97,0,0)


GREEN_YOUNG = (0,255,0)
GREEN_ADULT = (0,159,0)
GREEN_OLD = (0,97,0)
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
PREY_VALUE = 2
PREDATOR_VALUE = 1

PREY_PERCENTAGE = PREY_VALUE / 100
PREDATOR_PERCENTAGE = PREDATOR_VALUE / 100
PREY_CELLS = (int) (NX * NY * PREY_PERCENTAGE)
PREDATOR_CELLS = (int) (NX * NY * PREDATOR_PERCENTAGE)

# Reproduction and growth values (this will be moved into another .py in the future when i implement the GUI)
# ------------------------------------------------------------------------
TIMESIM = 0.1

#Reproduction
TIMEPREY = 4
TIMEPREDATOR = 4

PRE_REPRO_CONDITION = 3
PRE_REPRO_RATE = 2

#Growth
YOUNG_PREY_LIMIT = 10
ADULT_PREY_LIMIT = 20
DIE_PREY_LIMIT = 40

YOUNG_PREDATOR_LIMIT = 10
ADULT_PREDATOR_LIMIT = 30
DIE_PREDATOR_LIMIT = 40

# ------------------------------------------------------------------------
# Neighbors position vectors
# ------------------------------------------------------------------------
NEIGHBORS = 8
NY_COORD = [1,  1,  1, -1, -1, -1, 0 ,  0]
NX_COORD = [1,  0, -1,  1,  0, -1, 1 , -1]