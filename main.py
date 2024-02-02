# 
import pygame
from pygame.locals import *

import os

import agentpy as ap
import pathfinding as pf        #In case you want to use pathfinding algorithms for the agent's plan
import matplotlib.pyplot as plt
from owlready2 import *
import itertools
import random
#import IPython
import math

import IPython
import numpy as np

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Se carga el archivo de la clase Cubo
import sys, math
sys.path.append('Clases')
from Clases.Carro import Carro

from Clases.Edificio import Edificio

from objloader import *

screen_width = 500
screen_height = 500
#vc para el obser.
FOVY=60.0
ZNEAR=1.0
ZFAR=900.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X=300.0
EYE_Y=100.0
EYE_Z=300.0
CENTER_X=0
CENTER_Y=0
CENTER_Z=0
UP_X=0
UP_Y=1
UP_Z=0
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500
#Dimension del plano
DimBoard = 200
#Variables para el control del observador
theta = 0.0
radius = 100

#Arreglo para objetos
objetos = []

ontologia_file_path = "pFinal_onto.owl"

posiciones_entradas = np.array([[-220, -8],[220, 8],[-35, -220], [-48, 220], [-180, 220],[-166, -220], [166, 220], [180, -220]])
#Arreglo para el manejo de texturas
textures = []
filename1 = "Texturas/textura0.jpeg"
filename2 = "Texturas/textura1.jpeg"

pygame.init()

scale = 1.0

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    #Z axis in blue
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)

def lookat():
    global EYE_X
    global EYE_Z
    global radius
    EYE_X = radius * (math.cos(math.radians(theta)) + math.sin(math.radians(theta)))
    EYE_Z = radius * (-math.sin(math.radians(theta)) + math.cos(math.radians(theta)))
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)

def Texturas(filepath):
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image,"RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    
def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    Texturas(filename1)
    Texturas(filename2)
    
    glLightfv(GL_LIGHT0, GL_POSITION,  (0, 200, 0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded      
    
    objetos.append(OBJ("Objetos/SuperRoad.obj", swapyz=True))
    objetos[0].generate()
    objetos.append(OBJ("Objetos/Straightroad3.obj", swapyz=True))
    objetos[1].generate()
    objetos.append(OBJ("Objetos/Semaforo4.obj"))
    objetos[2].generate()

def draw_building(x, y, z, width, height, depth):
    #glColor3f(0.8, 0.8, 0.8)
    glBegin(GL_QUADS)
    glVertex3f(x - width / 2, y, z - depth / 2)
    glVertex3f(x - width / 2, y + height, z - depth / 2)
    glVertex3f(x + width / 2, y + height, z - depth / 2)
    glVertex3f(x + width / 2, y, z - depth / 2)

    glVertex3f(x - width / 2, y, z + depth / 2)
    glVertex3f(x - width / 2, y + height, z + depth / 2)
    glVertex3f(x + width / 2, y + height, z + depth / 2)
    glVertex3f(x + width / 2, y, z + depth / 2)

    glVertex3f(x - width / 2, y, z - depth / 2)
    glVertex3f(x - width / 2, y + height, z - depth / 2)
    glVertex3f(x - width / 2, y + height, z + depth / 2)
    glVertex3f(x - width / 2, y, z + depth / 2)

    glVertex3f(x + width / 2, y, z - depth / 2)
    glVertex3f(x + width / 2, y + height, z - depth / 2)
    glVertex3f(x + width / 2, y + height, z + depth / 2)
    glVertex3f(x + width / 2, y, z + depth / 2)
    glEnd()

""" def draw_street(x1, z1, x2, z2, width):
    glColor3f(0.5, 0.5, 0.5)
    glLineWidth(width)
    glBegin(GL_LINES)
    glVertex3f(x1, 0.1, z1)
    glVertex3f(x2, 0.1, z2)
    glEnd()
    glLineWidth(1.0) """

""" def draw_city():
    for i in range(-DimBoard + 50, DimBoard - 50, 100):
        for j in range(-DimBoard + 50, DimBoard - 50, 100):
            building_height = 50 + abs(i % 150) + abs(j % 150)
            draw_building(i, 0, j, 40, building_height, 40)

            # Draw streets along x-axis
            draw_street(i - 50, j, i + 50, j, 5)

            # Draw streets along z-axis
            draw_street(i, j - 50, i, j + 50, 5) """

def displayobj():
    glPushMatrix()  
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(173.0, 0.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[0].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(118.0, 0.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(65.0, 0.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(12.0, 0.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(-41.0, 0.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[0].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(-94.0, 0.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(-120.0, 0.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()
    
    glPushMatrix()  
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(-173.0, 0.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[0].render()  
    glPopMatrix()
    
    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(55.0, 173.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(110.0, 173.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(165.0, 173.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(173.0, 173.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()
    
    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(-55.0, 173.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(-110.0, 173.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(-165.0, 173.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(-173.0, 173.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()
    
    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(55.0, -41.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(110.0, -41.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(165.0, -41.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(173.0, -41.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()
    
    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(-55.0, -41.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(-110.0, -41.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(-165.0, -41.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(-173.0, -41.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()
    
    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(55.0, -173.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(110.0, -173.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(165.0, -173.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(173.0, -173.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()
    
    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(-55.0, -173.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(-110.0, -173.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(-165.0, -173.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()

    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(-173.0, -173.0, 3.0)
    glScale(6.0,6.0,6.0)
    objetos[1].render()  
    glPopMatrix()
    
    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glTranslatef(20.0, 0.0, 15.0)
    glScale(10.0, 10.0, 10.0)
    objetos[2].render()  
    glPopMatrix()
    
    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glTranslatef(20.0, 0.0, -186.0)
    glScale(10.0, 10.0, 10.0)
    objetos[2].render()  
    glPopMatrix()
    
    glPushMatrix()  
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glTranslatef(20.0, 0.0, 156.0)
    glScale(10.0, 10.0, 10.0)
    objetos[2].render()  
    glPopMatrix()
    
    glPushMatrix()  
    glRotatef(-180.0, 0.0, 1.0, 0.0)
    glTranslatef(60.0, 0.0, 26.0)
    glScale(10.0, 10.0, 10.0)
    objetos[2].render()  
    glPopMatrix()
    
    glPushMatrix()  
    glRotatef(-180.0, 0.0, 1.0, 0.0)
    glTranslatef(190.0, 0.0, 26.0)
    glScale(10.0, 10.0, 10.0)
    objetos[2].render()  
    glPopMatrix()
    
    glPushMatrix()  
    glRotatef(-180.0, 0.0, 1.0, 0.0)
    glTranslatef(-150.0, 0.0, 26.0)
    glScale(10.0, 10.0, 10.0)
    objetos[2].render()  
    glPopMatrix()
    
    glPushMatrix()  
    glRotatef(0.0, 0.0, 1.0, 0.0)
    glTranslatef(-150.0, 0.0, -40.0)
    glScale(10.0, 10.0, 10.0)
    objetos[2].render()  
    glPopMatrix()
    
    glPushMatrix()  
    glRotatef(0.0, 0.0, 1.0, 0.0)
    glTranslatef(195.0, 0.0, -40.0)
    glScale(10.0, 10.0, 10.0)
    objetos[2].render()  
    glPopMatrix()
    
    glPushMatrix()  
    glRotatef(0.0, 0.0, 1.0, 0.0)
    glTranslatef(-20.0, 0.0, -40.0)
    glScale(10.0, 10.0, 10.0)
    objetos[2].render()  
    glPopMatrix()
    
    
    #edificio 1
    glColor3f(10.3, 0.3, 0.3)
    draw_building(70.0, 0.0, 55.0, 30, 105, 30)
    draw_building(70.0, 0.0, 60.0, 30, 80, 30)
    draw_building(70.0, 0.0, 70.0, 30, 70, 30)
    
    #edificio 2
    glColor3f(1.5, 1.5, 0.5)
    draw_building(-95.0, 0.0, -55.0, 30, 105, 30)
    draw_building(-95.0, 0.0, -60.0, 30, 80, 30)
    draw_building(-95.0, 0.0, -70.0, 30, 70, 30)
    
    #edificio 2
    glColor3f(1.5, 1.5, 0.5)
    draw_building(-105.0, 0.0, 105.0, 30, 105, 30)
    draw_building(-105.0, 0.0, 110.0, 30, 80, 30)
    draw_building(-105.0, 0.0, 120.0, 30, 70, 30)
    
    
    #set de edificios 1
    glColor3f(0.0, 1.0, 1.0 )
    draw_building(70.0, 0.0, -40.0, 30, 105, 20)
    draw_building(90.0, 0.0, -40.0, 30, 80, 20)
    draw_building(110.0, 0.0, -40.0, 30, 70, 20)
    
    #set de edificios 
    glColor3f(0.0, 1.0, 1.0 )
    draw_building(-90.0, 0.0, 40.0, 30, 105, 20)
    draw_building(-110.0, 0.0, 40.0, 30, 80, 20)
    draw_building(-130.0, 0.0, 40.0, 30, 70, 20)
    
    #set de edificios 3
    glColor3f(1.5, 1.0, 0.5)
    draw_building(20.0, 0.0, 60.0, 30, 105, 20)
    draw_building(20.0, 0.0, -60.0, 30, 80, 20)
    draw_building(20.0, 0.0, -90.0, 30, 80, 20)
    draw_building(20.0, 0.0, -120.0, 30, 80, 20)
    draw_building(20.0, 0.0, 40.0, 30, 70, 20)
    
    #set de edificios 4
    glColor3f(10.3, 0.3, 0.3)
    draw_building(120.0, 0.0, -90.0, 30, 105, 20)
    draw_building(120.0, 0.0, -90.0, 30, 80, 20)
    draw_building(120.0, 0.0, -90.0, 30, 70, 20)
    
    #set de edificios 5
    glColor3f(10.3, 0.3, 0.3)
    draw_building(110.0, 0.0, 110.0, 30, 105, 20)
    draw_building(110.0, 0.0, 130.0, 30, 80, 20)
    draw_building(110.0, 0.0, 150.0, 30, 70, 20)
    
    
    #draw_building(60.0, 0.0, 26.0, 20, 85, 30)
    #draw_building(-190.0, 0.0, -40.0, 20, 100, 30)
    #draw_building(155.0, 0.0, -40.0, 30, 70, 30)


def PlanoTexturizado():
    #Activate textures
    glColor3f(1.0,1.0,1.0)
    glEnable(GL_TEXTURE_2D)
    #front face
    glBindTexture(GL_TEXTURE_2D, textures[0])    
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-DimBoard, 0, DimBoard)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(DimBoard, 0, DimBoard)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()              
    glDisable(GL_TEXTURE_2D)

def Paredes():
    # Pared frontal
    glColor3f(1.0, 1.0, 1.0)  
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-DimBoard - 100, 0, DimBoard + 100)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-DimBoard - 100, DimBoard , DimBoard + 100)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(DimBoard + 100, DimBoard , DimBoard + 100)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(DimBoard + 100, 0, DimBoard + 100)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    # Pared trasera
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-DimBoard - 100, 0, -DimBoard - 100)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-DimBoard - 100, DimBoard, -DimBoard - 100)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(DimBoard + 100, DimBoard, -DimBoard - 100)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(DimBoard + 100, 0, -DimBoard - 100)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    # Pared izquierda
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-DimBoard - 100, 0, -DimBoard - 100)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-DimBoard - 100, DimBoard, -DimBoard - 100)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-DimBoard - 100, DimBoard, DimBoard + 100)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-DimBoard - 100, 0, DimBoard + 100)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    # Pared derecha
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(DimBoard + 100, 0, -DimBoard - 100)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(DimBoard + 100, DimBoard, -DimBoard - 100)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(DimBoard + 100, DimBoard, DimBoard + 100)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(DimBoard + 100, 0, DimBoard + 100)
    glEnd()
    glDisable(GL_TEXTURE_2D)


def display():  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    PlanoTexturizado()
    Paredes()
    # Pared superior (cielo)
    glColor3f(0.53, 0.81, 0.92)  # Azul claro
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard - 100, DimBoard, -DimBoard - 100)
    glVertex3d(DimBoard + 100, DimBoard, -DimBoard - 100)
    glVertex3d(DimBoard + 100, DimBoard, DimBoard + 100)
    glVertex3d(-DimBoard - 100, DimBoard, DimBoard + 100)
    glEnd()
    
    # # Dibujar el piso verde
    glColor3f(0.0, 0.8, 0.0)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard - 100, -1, -DimBoard - 100)
    glVertex3d(-DimBoard - 100, -1, DimBoard + 100)
    glVertex3d(DimBoard + 100, -1, DimBoard + 100)
    glVertex3d(DimBoard + 100, -1, -DimBoard - 100)
    glEnd()
    displayobj()
    #draw_city()
'''    #Se dibuja el plano gris
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()'''

def handle_keys():
    global CENTER_X, CENTER_Y, CENTER_Z, EYE_Y, theta

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if theta < 1.0:
            theta = 360.0
        else:
            theta += -1.0
        lookat()
    if keys[pygame.K_RIGHT]:
        if theta > 359.0:
            theta = 0
        else:
            theta += 1.0
        lookat()
    if keys[pygame.K_UP]:
        EYE_Y += 1.0
        glLoadIdentity()
        gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    if keys[pygame.K_DOWN]:
        EYE_Y -= 1.0
        glLoadIdentity()
        gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)

if os.path.exists(ontologia_file_path):
    os.remove(ontologia_file_path)
    print(f"Archivo {ontologia_file_path} existente eliminado.")

onto = get_ontology("file://./pFinal_onto.owl")
#Definicion de Ontologia
with onto:

    #My SuperClass
    class Entity(Thing):
        pass

    class Car(Entity):
        pass

    class Traffic_light(Entity):
        pass

    class Place(Thing):
        pass

    #Propiedad que especifica la posicion del objeto
    class at_position(DataProperty,FunctionalProperty):
      domain = [Place]
      range = [str]
      pass

    #Estado del semaforo (Colores)
    class traffic_light_state(DataProperty):
      domain = [Traffic_light]
      range = [str]

    #Velocidad del carro
    class has_speed_car(DataProperty):
      domain = [Car]
      range = [float]

    #Propiedad para describir los carros que tenga adelante
    class cars_within_reach(ObjectProperty):
      domain = [Traffic_light]
      range = [int]

    #Property to describe the place of an entity in the world
    class is_in_place(ObjectProperty):
      domain = [Entity]
      range = [Place]

    class controls_traffic_light(ObjectProperty):
      domain = [Traffic_light]
      range = [Car]
      cardinality = [1, None]

    #Relacion carro y semaforo
    class is_controlled_by_traffic_light(ObjectProperty):
      domain = [Car]
      range = [Traffic_light]
      inverse_property = controls_traffic_light
      cardinality = [0, 1]

    onto.save()

class CarAgent(ap.Agent):

    def suscribe_traffic_light(self, tl):
        self.msg = None
        tl.carros_suscritos.append(self)
        pass

    def check_traffic_light(self, msg):
        self.msg = msg
   
    def see(self, e):
        pass
    
    def brf(self, p):
       pass

    def options(self):
       pass

    def filter(self):
       pass

    def plan(self):
       pass

    def BDI(self, p):
       pass

    def execute(self):
       pass

    def initBeliefs(self, initPos):
       pass

    def initIntentions(self):
       pass

    #======================Funciones Principales=======================

    def setup(self):
        self.carro = None
        self.msg = None
        self.moving = True

        self.rect = pygame.Rect(0, 0, 10, 5)
    
        pass

    def step(self):
       # Dibujo del carro
        self.carro.draw()

        self.rect.x = self.carro.Position[0]
        self.rect.y = self.carro.Position[1]
        pass

    def update(self):
       pass

    def end(self):
       pass

class SemaforoAgent(ap.Agent):

    def notify(self, mensaje):
        for carro in self.carros_suscritos:
            carro.check_traffic_light(mensaje)
        pass

    def setup(self):
        self.semaforo = None
        self.estado = 0 # 0 = rojo, 1 = amarillo, 2 = verde
        self.tiempo_cambio = 0.0
        self.carros_suscritos = []
        pass

    def step(self):
    
        if(self.tiempo_cambio == 30):
            self.estado = 2
        elif(self.tiempo_cambio == 60):
            self.estado = 1
        elif(self.tiempo_cambio == 70):
            self.estado = 0
            self.tiempo_cambio = 0

        self.tiempo_cambio += 1.0

        mensaje = self.estado
        self.notify(mensaje)
       
        pass

    def update(self):
       pass

    def end(self):
       pass

class Ciudad(ap.Model):
    def setup(self):
        # Se inicializa todas las variables de control
        Init()
        # Se generan los agentes junto con su instancia de carro
        self.carros = ap.AgentList(self, self.p.carros, CarAgent)
        for i, agente in enumerate(self.carros):
            # Asegúrate de que haya suficientes posiciones en la lista
            if i < len(posiciones_entradas):
                x, y = posiciones_entradas[i]
                agente.carro = Carro(1, self.carros, x, y)

                if y > 200:
                    # Aplicar rotación de 180 grados
                    agente.carro.Rotation = 180.0
                    agente.carro.has_rotated = True
                    agente.carro.Direction[0] *= 0
                    agente.carro.Direction[1] *= -1
                elif y < -200:
                    agente.carro.has_rotated = True
                    agente.carro.Direction[0] *= 0
                    agente.carro.Direction[1] *= 1
                elif x > 200:
                    agente.carro.Rotation = 90.0
                    agente.carro.has_rotated = True
                    agente.carro.Direction[0] *= -1
                    agente.carro.Direction[1] *= 0
                elif x < -200:
                    agente.carro.Rotation = -90.0
                    agente.carro.has_rotated = True
                    agente.carro.Direction[0] *= 1
                    agente.carro.Direction[1] *= 0

            else:
                # O maneja la situación si hay menos posiciones de las esperadas
                print("No hay suficientes posiciones predefinidas para todos los carros.")

    def step(self):
        handle_keys()
        display()
        displayobj()

        for carro in self.carros:
           carro.step()
        
        pygame.display.flip()
        pygame.time.wait(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end()

        pass

    def update(self):
       pass

    def end(self):
       pygame.quit()
       sys.exit()

parameters = {
   "steps": 5000,
   "carros": 8
}

model = Ciudad(parameters)
model.run()

# print("Clases en la ontología:")
# for cls in onto.classes():
#     print(cls)

# print("\nPropiedades en la ontología:")
# for prop in onto.properties():
#     print(prop)
