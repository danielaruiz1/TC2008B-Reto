import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import random
import math
from objloader import *

class Carro:
    def __init__(self, vel, carros, x, y):
        self.listCarros = carros
        self.vel = vel
        self.Rotation = 0.0
        self.has_rotated = False
        
        self.Position = [x, y, 5]
        self.Direction = [random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), 5]

        m = math.sqrt(self.Direction[0]**2 + self.Direction[2]**2)
        self.Direction[0] /= m
        self.Direction[2] /= m
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

        # Definir el rectángulo
        self.rect = pygame.Rect(self.Position[0], self.Position[1], 10.0, 5.0)

    def rotate(self, angle):
        glRotatef(angle, 0.0, 0.0, 1.0)

    def draw(self):
        glPushMatrix()

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

        # Actualizar el rectángulo
        self.rect.x = new_x
        self.rect.y = new_y

        # Verificar colisiones con otros objetos
        for otro_objeto in self.listCarros:
            if self.rect.colliderect(otro_objeto.rect):
                if(otro_objeto.rect[0] != self.rect[0] and otro_objeto.rect[1] != self.rect[1]):
                    self.Direction = [0, 0, 0]
                    print("colision")
                    print(f"Rectángulo actual: {self.rect}")
                    print(f"Rectángulo del otro objeto: {otro_objeto.rect}")
                    break  # Termina el bucle si hay una colisión
        else:
            # No hay colisión, actualiza la posición
            self.Position[0] = new_x
            self.Position[1] = new_y





