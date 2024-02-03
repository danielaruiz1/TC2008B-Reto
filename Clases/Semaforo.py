
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import random
import math
from objloader import *

class Semaforo:
    def __init__(self, x, y, rot):
        self.Rotacion = rot
        self.Position = [x, y, 0.0]  

        try:
            self.objeto = OBJ("Objetos/Semaforo4.obj", swapyz=True)
            if self.objeto is not None:
                self.objeto.generate()
            else:
                print("Error: No se pudo cargar el objeto.")
        except Exception as e:
            print(f"Error al cargar el objeto: {e}")

    def draw_hitbox_Light(self):
        glPushMatrix()
        glTranslatef(2.0, 5.7, 0.0)
        glScale(1.0, 1.0, 1.0)
        
        # Dibujar el hitbox
        glColor3f(1.0, 0.0, 0.0)  
        glBegin(GL_QUADS)
        glVertex3f(-1.0, 0.0, -1.0)
        glVertex3f(-1.0, 0.0, 1.0)
        glVertex3f(1.0, 0.0, 1.0)
        glVertex3f(1.0, 0.0, -1.0)
        glEnd()

        glPopMatrix()

    def draw_hitbox_side(self):
        glPushMatrix()
        glTranslatef(2.0, 0.5, 0.0)
        glScale(1.0, 1.0, 1.0)
        
        # Dibujar el hitbox
        glColor3f(0.0, 1.0, 0.0)  
        glBegin(GL_QUADS)
        glVertex3f(-1.0, 0.0, -1.0)
        glVertex3f(-1.0, 0.0, 1.0)
        glVertex3f(1.0, 0.0, 1.0)
        glVertex3f(1.0, 0.0, -1.0)
        glEnd()

        glPopMatrix()

    def draw(self):
        glPushMatrix()
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        glRotatef(self.Rotacion, 0.0, 0.0, 1.0)
        glTranslatef(self.Position[0], self.Position[1], 0.0)
        glScale(7.0, 7.0, 7.0)
        self.objeto.render()
        glPopMatrix()
    
