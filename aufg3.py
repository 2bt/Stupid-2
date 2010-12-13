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

def face_voodoo(f):
	m = (f.split("/") + [0, 0])[:3]
	return tuple(int(i) if i else None for i in m)

class ObjObject:

	def __init__(self, filename):
		self.vertices = v = []
		self.normals = n = []
		self.textures = t = []
		self.faces = f = []

		actions = {
			"v" : lambda x : v.append(tuple(float(i) for i in x)),
			"vn" : lambda x : n.append(tuple(float(i) for i in x)),
			"vt" : lambda x : t.append(tuple(float(i) for i in x)),
			"f" : lambda x : f.append(tuple(face_voodoo(i) for i in x))
		}
		for line in open(filename):
			x = line.split()
			if x:
				a = x[0]
				if a in actions: actions[a](x[1:])

		self.gen_list()

	def gen_list(self):
		self.display_list = glGenLists(1)
		glNewList(self.display_list, GL_COMPILE)
		self.render_raw()
		glEndList()
		return self.display_list

	def render(self):
		glCallList(self.display_list)

	def render_raw(self):
		for face in self.faces:
			glBegin(GL_TRIANGLE_FAN)
			for v, t, n in face:
				if n: glNormal(*self.normals[n - 1])
				glVertex(self.vertices[v - 1])
			glEnd()


class Squeeze(Entity):
	def __init__(self):
		Entity.__init__(self)
		self.obj = ObjObject("datasets/bunny.obj")

	def render_sub(self):
		glColor(1, 1, 0)
		self.obj.render()

if __name__ == "__main__":

	stupid = Stupid("Stupid [ CGI - Aufgabe 3 ]")
	stupid.add(Squeeze())
	stupid.mainloop()


