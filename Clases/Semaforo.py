
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import random
import math

import sys
sys.path.append('..')
from objloader import *

class Semaforo:
    def __init__(self, x, y, rot, light):
        self.Rotacion = rot
        self.Position = [x, y, 0.0]  
        self.Light = light
        self.hitbox_light = None
        self.hitbox_side = None
            
        try:
            self.objeto = OBJ("Objetos/Semaforo4.obj", swapyz=True)
            if self.objeto is not None:
                self.objeto.generate()
            else:
                print("Error: No se pudo cargar el objeto.")
        except Exception as e:
            print(f"Error al cargar el objeto: {e}")

    def draw(self):
        glPushMatrix()
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        glRotatef(self.Rotacion, 0.0, 0.0, 1.0)
        glTranslatef(self.Position[0], self.Position[1], 0.0)
        glScale(7.0, 7.0, 7.0)
        self.objeto.render()

        # glColor3fv((1, 0, 0))  # Color rojo para las hitboxes
        # if self.hitbox_light:
        #     print("hitbox_light")
        #     self.draw_hitbox(self.hitbox_light)
        # if self.hitbox_side:
        #     print("hitbox_side")
        #     self.draw_hitbox(self.hitbox_side)

        glPopMatrix()

    def draw_hitbox(self, hitbox):
        print(hitbox.position[0])
        glPushMatrix()
        glTranslatef(hitbox.position[0], hitbox.position[1], hitbox.position[2])
        glTranslatef(0,0,0)
        glScalef(1,1,1)

        # Dibujar el cubo usando líneas
        glBegin(GL_LINES)
        # Cara frontal
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)

        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)

        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)

        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, -0.5, -0.5)

        # Conexiones entre caras
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5, 0.5)

        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, 0.5)

        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, 0.5)

        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, 0.5)

        # Cara trasera
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)

        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)

        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)

        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)

        glEnd()

        glPopMatrix()
    
