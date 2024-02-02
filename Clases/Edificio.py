import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math
import numpy as np

class Edificio:
    def __init__(self):
        pass
    
    def draw_building(self, x, y, z, width, height, depth, texture):
        id = 1
        glPushMatrix()
        glColor3f(0.8, 0.8, 0.8)
        glEnable(GL_TEXTURE_2D)
        #front face
        glBindTexture(GL_TEXTURE_2D, texture[id])
        glBegin(GL_QUADS)
        glBindTexture(GL_TEXTURE_2D, texture[id])
        glVertex3f(x - width / 2, y, z - depth / 2)
        glBindTexture(GL_TEXTURE_2D, texture[id])
        glVertex3f(x - width / 2, y + height, z - depth / 2)
        glBindTexture(GL_TEXTURE_2D, texture[id])
        glVertex3f(x + width / 2, y + height, z - depth / 2)
        glBindTexture(GL_TEXTURE_2D, texture[id])
        glVertex3f(x + width / 2, y, z - depth / 2)
        
        glBindTexture(GL_TEXTURE_2D, texture[id])
        glVertex3f(x - width / 2, y, z + depth / 2)
        glBindTexture(GL_TEXTURE_2D, texture[id])
        glVertex3f(x - width / 2, y + height, z + depth / 2)
        glBindTexture(GL_TEXTURE_2D, texture[id])
        glVertex3f(x + width / 2, y + height, z + depth / 2)
        glBindTexture(GL_TEXTURE_2D, texture[id])
        glVertex3f(x + width / 2, y, z + depth / 2)

        glBindTexture(GL_TEXTURE_2D, texture[id])
        glVertex3f(x - width / 2, y, z - depth / 2)
        glBindTexture(GL_TEXTURE_2D, texture[id])
        glVertex3f(x - width / 2, y + height, z - depth / 2)
        glBindTexture(GL_TEXTURE_2D, texture[id])
        glVertex3f(x - width / 2, y + height, z + depth / 2)
        glBindTexture(GL_TEXTURE_2D, texture[id])
        glVertex3f(x - width / 2, y, z + depth / 2)

        glBindTexture(GL_TEXTURE_2D, texture[id])
        glVertex3f(x + width / 2, y, z - depth / 2)
        glBindTexture(GL_TEXTURE_2D, texture[id])
        glVertex3f(x + width / 2, y + height, z - depth / 2)
        glBindTexture(GL_TEXTURE_2D, texture[id])
        glVertex3f(x + width / 2, y + height, z + depth / 2)
        glBindTexture(GL_TEXTURE_2D, texture[id])
        glVertex3f(x + width / 2, y, z + depth / 2)
        glDisable(GL_TEXTURE_2D)
        glEnd()
        glPopMatrix()

    