
import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
import random
import math

from objloader import *

class Carro:

    def __init__(self, vel):
        self.vel = vel
        self.Position = []
        self.Position.append(1)
        self.Position.append(1)
        self.Position.append(1)
        
        self.Direction = []
        self.Direction.append(random.random())
        self.Direction.append(10)
        self.Direction.append(random.random())

        m = math.sqrt(self.Direction[0]*self.Direction[0] + self.Direction[2]*self.Direction[2])
        self.Direction[0] /= m
        self.Direction[2] /= m
        #Se cambia la maginitud del vector direccion
        self.Direction[0] *= vel
        self.Direction[2] *= vel

        try:
            self.objeto = OBJ("Objetos/Camaro.obj", swapyz=True)
            if self.objeto is not None:
                self.objeto.generate()
            else:
                print("Error: No se pudo cargar el objeto.")
        except Exception as e:
            print(f"Error al cargar el objeto: {e}")
        
    def draw(self):
        glPushMatrix()  
        #correcciones para dibujar el objeto en plano XZ
        #esto depende de cada objeto
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        glTranslatef(0.0, 0.0, 5.0)
        glScale(2.0,2.0,2.0)
        self.objeto.render()  
        glPopMatrix()
    
    # def update(self):
    #     new_x = self.Position[0] + self.Direction[0]
    #     new_z = self.Position[2] + self.Direction[2]

    #     self.Position[0] = new_x
    #     self.Position[2] = new_z



