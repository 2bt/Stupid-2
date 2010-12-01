#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from stupid import Stupid, Entity
import math
import font
import savage as shit
from vec import vec



class Contra(Entity):

	def __init__(self):
		Entity.__init__(self)
		self.cube = shit.Brick(1, 1, 1).gen_list()


	def render_sub(self):

		glPushMatrix()
		q = vec(0, 0, -0.5)
		glMultMatrixf([
			1, 0, 0, q.x,
			0, 1, 0, q.y,
			0, 0, 1, q.z,
			0, 0, 0, 1
		])
		glColor(1, 1, 0)
		glCallList(self.cube)
		glPopMatrix()

		glColor(1, 1, 1, 0.4)
		glCallList(self.cube)


class Suck(Entity):

	def __init__(self):
		Entity.__init__(self)

		self.orb = shit.Orb(1).gen_list()
		self.r = 0

	def update_sub(self, time_dif):
		self.r += time_dif * 10

	def render_sub(self):
		glRotate(self.r, 0, 1, 0)
		glCallList(self.orb)



if __name__ == "__main__":

	stupid = Stupid("Stupid [ CGI - Aufgabe 2 ]")
	stupid.add(Contra())
	stupid.add(Suck())
	stupid.mainloop()


