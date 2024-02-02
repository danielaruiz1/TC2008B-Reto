# 
import pygame
from pygame.locals import *

import agentpy as ap
import pathfinding as pf        #In case you want to use pathfinding algorithms for the agent's plan
import matplotlib.pyplot as plt
from owlready2 import *
import itertools
import random
#import IPython
import math

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Se carga el archivo de la clase Cubo
import sys, math
sys.path.append('..')
#from Ciudad import Ciudad

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
EYE_Y=200.0
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
radius = DimBoard + 20

#Arreglo para objetos
objetos = []
#Arreglo para el manejo de texturas
textures = []
filename1 = "TC2008B/textura0.jpeg"

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
    
    glLightfv(GL_LIGHT0, GL_POSITION,  (0, 200, 0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
<<<<<<< HEAD
    glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded      
    
    objetos.append(OBJ("TC2008B-Reto/Objetos/SuperRoad.obj", swapyz=True))
=======
    glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded        
    objetos.append(OBJ("Objetos/SuperRoad.obj", swapyz=True))
>>>>>>> 446bcf10fb43e6f71d64dab882bbe82654ac92c2
    objetos[0].generate()
    objetos.append(OBJ("Objetos/Straightroad3.obj", swapyz=True))
    objetos[1].generate()
<<<<<<< HEAD
=======
    objetos.append(OBJ("Objetos/Semaforo4.obj"))
    objetos[2].generate()
>>>>>>> 446bcf10fb43e6f71d64dab882bbe82654ac92c2

def draw_building(x, y, z, width, height, depth):
    glColor3f(0.8, 0.8, 0.8)
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
    draw_building(70.0, 0.0, 55.0, 30, 105, 30)
    draw_building(70.0, 0.0, 60.0, 30, 80, 30)
    draw_building(70.0, 0.0, 70.0, 30, 70, 30)
    #edificio 2
    draw_building(-95.0, 0.0, -55.0, 30, 105, 30)
    draw_building(-95.0, 0.0, -60.0, 30, 80, 30)
    draw_building(-95.0, 0.0, -70.0, 30, 70, 30)
    
    #edificio 2
    draw_building(-105.0, 0.0, 105.0, 30, 105, 30)
    draw_building(-105.0, 0.0, 110.0, 30, 80, 30)
    draw_building(-105.0, 0.0, 120.0, 30, 70, 30)
    
    
    #set de edificios 1
    draw_building(70.0, 0.0, -40.0, 30, 105, 20)
    draw_building(90.0, 0.0, -40.0, 30, 80, 20)
    draw_building(110.0, 0.0, -40.0, 30, 70, 20)
    
    #set de edificios 2
    draw_building(-90.0, 0.0, 40.0, 30, 105, 20)
    draw_building(-110.0, 0.0, 40.0, 30, 80, 20)
    draw_building(-130.0, 0.0, 40.0, 30, 70, 20)
    
    #set de edificios 3
    draw_building(20.0, 0.0, 60.0, 30, 105, 20)
    draw_building(20.0, 0.0, -60.0, 30, 80, 20)
    draw_building(20.0, 0.0, -90.0, 30, 80, 20)
    draw_building(20.0, 0.0, -120.0, 30, 80, 20)
    draw_building(20.0, 0.0, 40.0, 30, 70, 20)
    
    #set de edificios 4
    draw_building(120.0, 0.0, -90.0, 30, 105, 20)
    draw_building(120.0, 0.0, -90.0, 30, 80, 20)
    draw_building(120.0, 0.0, -90.0, 30, 70, 20)
    
    #set de edificios 5
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


def display():  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    PlanoTexturizado()
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
        

done = False
Init()
while not done:
    handle_keys()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    display()

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()