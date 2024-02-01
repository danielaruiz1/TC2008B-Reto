
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
        self.Rotation = 0.0  # Nueva propiedad para almacenar la rotación
        self.has_rotated = False  # Nueva propiedad para rastrear si ya ha rotado
        self.Position = []
        self.Position.append(0)
        self.Position.append(0)
        self.Position.append(5)
        
        self.Direction = []
        self.Direction.append(random.uniform(0.5, 1.0))
        self.Direction.append(random.uniform(0.5, 1.0))
        self.Direction.append(5)

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
        
    def rotate(self, angle):
        glRotatef(angle, 0.0, 0.0, 1.0)
    
    def draw(self):
        glPushMatrix()  

        # Traslación sin cambios en el eje Z
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        glTranslatef(self.Position[0], self.Position[1], 5.0)
        glScalef(2.0, 2.0, 2.0)
        glRotatef(self.Rotation, 0.0, 0.0, 1.0)
        self.objeto.render()  

        glPopMatrix()
        self.update()
    
    def update(self):
        new_x = self.Position[0] + self.Direction[0]
        new_y = self.Position[1] + self.Direction[1]
        
        self.Position[0] = new_x
        self.Position[1] = new_y

    



