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



class Suck(Entity):

	def __init__(self):
		Entity.__init__(self)

		self.orb = shit.Orb(5).gen_list()

	def update_sub(self, time_dif):
		pass

	def render_sub(self):
		glCallList(self.orb)



if __name__ == "__main__":

	stupid = Stupid("Stupid [ CGI - Aufgabe 2 ]")
	stupid.add(Suck())
	stupid.mainloop()


