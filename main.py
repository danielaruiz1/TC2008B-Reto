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
from Clases.Semaforo import Semaforo

from objloader import *

screen_width = 500
screen_height = 500
#vc para el obser.
FOVY=60.0
ZNEAR=1.0
ZFAR=900.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X=200.0
EYE_Y=180.0
EYE_Z=200.0
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
radius = 200

#Arreglo para objetos
objetos = []

ontologia_file_path = "pFinal_onto.owl"

posiciones_entradas = np.array([[-220.0, -8.0],[220.0, 8.0],[-35.0, -220.0], [-48, 220.0], [-180.0, 220.0],[-166.0, -220.0], [166.0, 220.0], [180.0, -220.0]])
posiciones_finales = np.array([[220.0, -8.0], [-220.0, 8.0], [-35.0, 220.0], [-48, -220.0], [-180.0, -220.0], [-166.0, 220.0], [166.0, -220.0], [180.0, 220.0]])

posiciones_semaforos = np.array([[-25.0, 150.0, 90.0, 2], [-25.0, -197.0, 90.0, 2], [-25.0, 17.0, 90.0, 2],
                                 [17.0, -25.0, 180.0, 0], [150.0, -25.0, 180.0, 0], [-197.0, -25.0, 180.0, 0],
                                 [-67.0, -25.0, 0.0, 0], [-197.0, -25.0, 0.0, 0], [150.0, -25.0, 0.0, 0],
                                 [-25.0, -197.0, -90, 2], [-25.0, 150.0, -90.0, 2],[-25.0, -67.0, -90.0, 2],])

#Arreglo para el manejo de texturas
textures = []
filename1 = "Texturas/textura0.jpeg"
filename2 = "Texturas/textura3.jpg"

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
    glTexCoord2f(0.0, 1.0)  
    glVertex3f(-DimBoard - 100, 0, DimBoard + 100)
    glTexCoord2f(0.0, 0.0)  
    glVertex3f(-DimBoard - 100, DimBoard , DimBoard + 100)
    glTexCoord2f(1.0, 0.0)  
    glVertex3f(DimBoard + 100, DimBoard , DimBoard + 100)
    glTexCoord2f(1.0, 1.0)  
    glVertex3f(DimBoard + 100, 0, DimBoard + 100)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    # Pared trasera
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0) 
    glVertex3f(-DimBoard - 100, 0, -DimBoard - 100)
    glTexCoord2f(0.0, 0.0) 
    glVertex3f(-DimBoard - 100, DimBoard, -DimBoard - 100)
    glTexCoord2f(1.0, 0.0) 
    glVertex3f(DimBoard + 100, DimBoard, -DimBoard - 100)
    glTexCoord2f(1.0, 1.0) 
    glVertex3f(DimBoard + 100, 0, -DimBoard - 100)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    # Pared izquierda
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0) 
    glVertex3f(-DimBoard - 100, 0, -DimBoard - 100)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-DimBoard - 100, DimBoard, -DimBoard - 100)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-DimBoard - 100, DimBoard, DimBoard + 100)
    glTexCoord2f(1.0, 1.0) 
    glVertex3f(-DimBoard - 100, 0, DimBoard + 100)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    # Pared derecha
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0) 
    glVertex3f(DimBoard + 100, 0, -DimBoard - 100)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(DimBoard + 100, DimBoard, -DimBoard - 100)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(DimBoard + 100, DimBoard, DimBoard + 100)
    glTexCoord2f(1.0, 1.0)
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

    #Estado del semaforo (Colores)
    class traffic_light_state(DataProperty):
      domain = [Traffic_light]
      range = [str]

    class fellow_car_intention(ObjectProperty):
        domain = [Car]
        range = [int]

    #Velocidad del carro
    class has_speed_car(DataProperty):
      domain = [Car]
      range = [float]

    class has_direction_car(DataProperty):
      domain = [Car]
      range = [float]

    #Propiedad para describir los carros que tenga el semaforo
    class cars_within_reach(ObjectProperty):
      domain = [Traffic_light]
      range = [int]

    #Propiedad para describir los carros que tenga adelante
    class cars_nearby(ObjectProperty):
      domain = [Car]
      range = [str]

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
        # self.msg = None
        tl.carros_suscritos.append(self)

    def check_traffic_light(self, msg):
        self.msg = msg
   
    def see(self, e):
        new_x = self.carro.Position[0] + self.carro.Direction[0]
        new_y = self.carro.Position[1] + self.carro.Direction[1]

        new_hitbox = Hitbox3D(position=[new_x, new_y, 5], size=[10, 10, 5])
        
        p = [[],[]]

        for objeto in e:
            if objeto != self:  # Excluir la instancia actual del agente
                if hasattr(objeto, 'semaforo'):
                    if self.crossing != True:
                        if self not in objeto.carros_suscritos:
                            if new_hitbox.collides_with(objeto.hitbox_light):
                                self.suscribe_traffic_light(objeto)
                        else: 
                            if self.msg == 0:
                                p = [objeto, "light", "stop"]
                                break
                            else:
                                p = [objeto, "light", "go"]
                                break
                    else:
                        if new_hitbox.collides_with(objeto.hitbox_side):
                            p = [objeto, "side"]
                            if self in objeto.carros_suscritos:
                                objeto.carros_suscritos.remove(self)
                            break

                elif hasattr(objeto, "carro"):
                    x, y, _ = self.carro.Position
                    x2, y2, _ = objeto.carro.Position
                    distancia = math.sqrt((x2 - x)**2 + (y2 - y)**2)

                    # if(objeto.crossing == False and self.crossing == True):
                    #     '''Esto para evitar que un carro avance cuando uno este en medio
                    #    pues el problema principal son las velocidades'''
                    #     if (distancia <= 16):
                    #         # Se debe detener
                    #         # Probable hace falta ajustar la distancia
                    #         print("detuvo")
                    #         self.moving = False
                    #         #self.carro.Direction = [0,0,0]
                    #         pass
                    # elif(objeto.crossing == True and self.crossing == True):
                    #     '''Cuando el carro y otro mas esten dentro de las interseccion
                    #     se pueda decidir cual va primero'''
                    #     #self.carro.Direction = self.carro.PastDirection
                    #     self.moving = True
                    #     if (distancia <= 20):
                    #         print("carro dentro detenido")
                    #         p = [objeto, "carro"]
                    #         self.moving = False
                    # else:
                    #     self.moving = True    
        return p
    
    def brf(self, p):
       # Revisar el semaforo
        currentPos = self.carro.Position
        self.this_car.is_in_place = [Place(at_position = str(currentPos))]

        if(p[1] == "light"):
            if(p[2] == "stop"):
                self.moving = False
            else:
                self.moving = True
                self.crossing = True
            self.intentionSucceded = True
            print("toco semaforo")
        elif(p[1] == "side"):
            print("Toco")
            self.crossing = False
        elif(p[1] == "carro"):
            # if(self.action == 0 and p[0].action == 0):
            #     self.moving = True
            #     # Avance sin problema
            #     pass
            # elif(self.action == 1 and p[0].action != 2):
            #     self.moving = True
            #     # Avance sin problemas
            #     pass
            # elif(self.action == 2):
            #     self.moving = False
            #     # Detenerse
            #     pass
            pass

    def options(self):
        # Que acciones puede realizar
        # Saca las tres opciones que puede sacar
        # 0 = Adelante, 1 = Derecha, 2 = Izquierda
        return [0,1,2]

    def filter(self, options):
        # Que accion va realizar
        # En este caso puede ser aleatorio
        return random.choice(options)
        #return 0
        pass

    def plan(self, selected_option):
        # Guardar la opcion que salio del filter aqui
        return selected_option 
       
    def BDI(self, p):
       self.brf(p)

       if self.intentionSucceded:
           self.intentionSucceded = False
           self.D = self.options()
           self.I = self.filter(self.D)
           self.currentPlan = self.plan(self.I)

    def execute(self):
        # Ejecutar el plan
        if self.moving:
            if not self.crossing:
                self.currentPlan = 0

            if self.currentPlan == 0:
                self.move_forward()
            elif self.currentPlan == 1:
                self.rotate_and_move(-90)
            elif self.currentPlan == 2:
                self.rotate_and_move(90)
                #self.move_forward()

    def move_forward(self):
        self.carro.Position = [
            self.carro.Position[0] + self.carro.Direction[0],
            self.carro.Position[1] + self.carro.Direction[1],
            5
        ]
        self.rotation_done = False

    def rotate_and_move(self, angle):
        if not hasattr(self, 'distance_traveled'):
            self.distance_traveled = 0

        if angle == 90:
            distancia_deseada = 37
        elif angle == -90:
            distancia_deseada = 22
        else:
            return  # Manejar otros ángulos no implementado

        if self.distance_traveled < distancia_deseada:
            self.move_forward()
            self.distance_traveled += np.linalg.norm(self.carro.Direction[:2])  # Distancia en el plano XY
            self.rotation_done = False

            print("Avanzando. Distancia recorrida:", self.distance_traveled)
        else:
            if not self.rotation_done:
                self.carro.Rotation += angle
                self.carro.Rotation %= 360  # Asegurar que el ángulo esté en el rango [0, 360)
                self.rotation_done = True  # Marcar que el giro se ha completado

                print("Girando. Nuevo ángulo:", self.carro.Rotation)

            # Ajustar la dirección utilizando la función de rotación de NumPy
            if self.rotation_done:
                print("done")
                angle_radians = math.radians(angle)
                rotation_matrix = np.array([[np.cos(angle_radians), -np.sin(angle_radians)],
                                        [np.sin(angle_radians), np.cos(angle_radians)]])

                # Aplicar la rotación a la dirección (solo en el plano XY)
                rotated_direction = np.dot(rotation_matrix, self.carro.Direction[:2])
                self.carro.Direction[0] = rotated_direction[0]
                self.carro.Direction[1] = rotated_direction[1]

                print("EEEEEEEEE: ", self.moving)

                self.distance_traveled = 0  # Reiniciar la distancia después del giro completo
                print("Dirección ajustada después del giro:", self.carro.Direction)
                self.currentPlan = 0
                self.move_forward()

    def initBeliefs(self, initPos):

        place = Place(at_position=str(initPos))

        '''No tiene mucho sentido pues la instancia de carro
           se puede ver en la variable self.carro'''
        
        self.this_car = Car(is_in_place = [place])
        self.this_car.has_direction_car = list(self.carro.Direction)
        self.this_car.has_speed_car = [self.carro.vel]

    def initIntentions(self):
       
       self.intentionSucceded = True
       self.I = None

    #======================Funciones Principales=======================

    def setup(self):
        self.carro = None
        self.msg = None
        self.action = 0 # 0 = Del., 1 = Der., 2 = Izq.
        self.crossing = False
        self.firstStep = True
        self.moving = True
        self.hitbox = Hitbox3D(position=[0, 0, 0], size=[10, 10, 5])  # Ajusta el tamaño según tus necesidades
        self.rotation_done = False
        self.d_travelled = 0

    def step(self):
       # Dibujo del carro
        self.carro.draw()

        if self.firstStep:
            initPos = self.carro.Position
            self.initBeliefs(initPos)
            self.initIntentions()
            self.firstStep = False

        self.BDI(self.see(self.model.carros + self.model.semaforos))

        self.execute()

        pass

    def update(self):
        pass


    def end(self):
       pass

class SemaforoAgent(ap.Agent):

    def notify(self, mensaje):
        carros_suscritos_en_model = [carro for carro in self.model.carros if carro in self.carros_suscritos]

        for carro in carros_suscritos_en_model:
            carro.check_traffic_light(mensaje)
        pass

    def set_semaforo_hitboxes(self, semaforo):
        self.semaforo = semaforo
        self.estado = semaforo.Light
        if self.semaforo and not self.hitbox_light:  # Verificar que haya un semáforo y el Hitbox3D no se haya creado
            if self.semaforo.Rotacion == 180:
                self.hitbox_light = Hitbox3D(position=[semaforo.Position[0] * -1 - 10, semaforo.Position[1] + 5, 10], size=[7, 7, 7])
                self.hitbox_side = Hitbox3D(position=[semaforo.Position[0] * -1 - 20, semaforo.Position[1] + 55, 10], size=[7, 7, 7])
            elif self.semaforo.Rotacion == 0:
                self.hitbox_light = Hitbox3D(position=[semaforo.Position[0] + 10, semaforo.Position[1] * -1 - 5, 10], size=[7, 7, 7])
                self.hitbox_side = Hitbox3D(position=[semaforo.Position[0] + 10, semaforo.Position[1] * -1 - 55, 10], size=[7, 7, 7])
            elif self.semaforo.Rotacion == 90:
                self.hitbox_light = Hitbox3D(position=[semaforo.Position[1] * -1 - 45, semaforo.Position[0] * -1 -40, 10], size=[7, 7, 7])
                self.hitbox_side = Hitbox3D(position=[semaforo.Position[1] * -1 + 5, semaforo.Position[0] * -1 - 30, 10], size=[7, 7, 7])
            elif self.semaforo.Rotacion == -90:
                self.hitbox_light = Hitbox3D(position=[semaforo.Position[1] + 45, semaforo.Position[0] * -1 - 10, 10], size=[7, 7, 7])
                self.hitbox_side = Hitbox3D(position=[semaforo.Position[1] - 5, semaforo.Position[0] + 40, 10], size=[7, 7, 7])
            
            self.semaforo.hitbox_light = self.hitbox_light
            self.semaforo.hitbox_side = self.hitbox_light

    def setup(self):
        self.semaforo = None
        self.estado = 0 # 0 = rojo, 1 = amarillo, 2 = verde
        self.tiempo_cambio = 0.0
        self.carros_suscritos = []
        self.hitbox_light = None 
        self.hitbox_side = None

    def step(self):
        self.semaforo.draw()
        self.update()
        pass

    def update(self):
        if self.tiempo_cambio == 30:
            for semaforo in self.model.semaforos:
                if semaforo.estado == 0:
                    semaforo.estado = -1
                elif semaforo.estado == 2:
                    semaforo.estado = 1
        if self.tiempo_cambio == 40:
            for semaforo in self.model.semaforos:
                if semaforo.estado == 1:
                    semaforo.estado = 0  
                elif semaforo.estado == -1:
                    semaforo.estado = 2        
        if self.tiempo_cambio == 70:
            for semaforo in self.model.semaforos:
                if semaforo.estado == 2:
                    semaforo.estado = 0
                elif semaforo.estado == 0:
                    semaforo.estado = 2    
            self.tiempo_cambio = 0
            
        self.tiempo_cambio += 1.0
        
        mensaje = self.estado
        self.notify(mensaje)
        pass

    def end(self):
       pass

class Ciudad(ap.Model):
    def setup(self):
        # Se inicializa todas las variables de control
        Init()
        # Se generan los agentes junto con su instancia de carro
        #self.carros = ap.AgentList(self, self.p.carros, CarAgent)
        self.carros = ap.AgentList(self, 4, CarAgent)
        self.semaforos = ap.AgentList(self, 12, SemaforoAgent)

        for i, agente in enumerate(self.semaforos):
            if i < len(posiciones_semaforos):
                x, z, rot, light = posiciones_semaforos[i]
                agente.semaforo = Semaforo(x, z, rot, light)
                agente.set_semaforo_hitboxes(agente.semaforo)

        for i, agente in enumerate(self.carros):
            # Asegúrate de que haya suficientes posiciones en la lista
            if i < len(posiciones_entradas):
                x, y = posiciones_entradas[i]
                agente.carro = Carro(6, self.carros, x, y)

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

        for semaforo in self.semaforos:
            semaforo.step()

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


class Hitbox3D:
    def __init__(self, position, size):
        self.position = np.array(position)
        self.size = np.array(size)

    def collides_with(self, other_hitbox):
        # Verifica si hay colisión entre dos hitboxes 3D
        min_distance = (self.size + other_hitbox.size) / 2
        distance = np.abs(self.position - other_hitbox.position)
        return np.all(distance < min_distance)
    

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
