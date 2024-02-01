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
import IPython

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Se carga el archivo de la clase Cubo
import sys, math
sys.path.append('Clases')
from Clases.Carro import Carro

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

carros = []
objetos = []

ontologia_file_path = "pFinal_onto.owl"

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

    glLightfv(GL_LIGHT0, GL_POSITION,  (0, 200, 0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)# most obj files expect to be smooth-shaded        
    
    carros.append(Carro(1))


""" def draw_building(x, y, z, width, height, depth):
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
    glEnd() """

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

def display():  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    #Se dibuja el plano gris
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()
    #draw_city()

    for obj in carros:
       obj.draw()
       #obj.update()

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

    class Pedestrian(Entity):
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

    #Velocidad del peaton
    class has_speed_pedestrian(DataProperty):
      domain = [Pedestrian]
      range = [float]

    #Propiedad para describir los carros que tenga adelante
    class cars_within_reach(ObjectProperty):
      domain = [Traffic_light]
      range = [int]

    #Property to describe the place of an entity in the world
    class is_in_place(ObjectProperty):
      domain = [Entity]
      range = [Place]
      pass

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

    class pedestrians_at_crosswalk(ObjectProperty):
        domain = [Traffic_light]
        range = [Pedestrian]
        cardinality = [0, None]

    #Relación entre peatones y semáforos
    class crosswalks_at(ObjectProperty):
        domain = [Pedestrian]
        range = [Traffic_light]
        inverse_property = pedestrians_at_crosswalk
        cardinality = [0, 1]
    
    onto.save()

class Car(ap.Agent):
   
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
        pass

    def update(self):
       pass

    def end(self):
       pass
   
class Peaton(ap.Agent):
    def setup(self):
        pass

    def step(self):
       pass

    def update(self):
       pass

    def end(self):
       pass   

class Semaforo(ap.Agent):
    def setup(self):
        pass

    def step(self):
       pass

    def update(self):
       pass

    def end(self):
       pass

class Ciudad(ap.Model):
    def setup(self):
        pass

    def step(self):
       pass

    def update(self):
       pass

    def end(self):
       pass


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

print("Clases en la ontología:")
for cls in onto.classes():
    print(cls)

print("\nPropiedades en la ontología:")
for prop in onto.properties():
    print(prop)

pygame.quit()