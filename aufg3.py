#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
import sys
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from stupid import Stupid, Entity
import math
import font
import savage as shit
from vec import vec


def face_surface(face):
	if len(face) != 3:
		raise NotImplementedError("Only triangles allowed")
	a = (face[1] - face[0]).size()
	b = (face[2] - face[0]).size()
	c = (face[1] - face[2]).size()
	s = (a + b + c) / 2
	return (s * (s - a) * (s - b) * (s - c)) ** 0.5

def surface(mesh):
	return sum(face_surface(face) for face in mesh.vect_faces())

def volume(mesh):
	return 1.0 / 6 * sum(a * b.cross(c) for a, b, c in mesh.vect_faces())








class ObjObject:

	def __init__(self, filename):
		self.vertices = v = []
		self.normals = n = []
		self.tex_coords = t = []
		self.faces = f = []

		def face_voodoo(f):
			m = (f.split("/") + [0, 0])[:3]
			return tuple(int(i) if i else None for i in m)

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
			if not face[0][2]:
				a, b, c = [vec(*self.vertices[f[0] - 1]) for f in face[:3]]
				ab = b - a
				ac = c - a
				try: glNormal(*ab.cross(ac).normalize())
				except ZeroDivisionError: pass
			for v, t, n in face:
				if n: glNormal(*self.normals[n - 1])
				glVertex(self.vertices[v - 1])
			glEnd()


	def save(self, filename):

		def face2str(f):
			if any(f[1:]):
				return '/'.join(str(i) if i else "" for i in f)
			else: return str(f[0])

		parts = [
			("v", self.vertices, str),
			("vn", self.normals, str),
			("vt", self.tex_coords, str),
			("f", self.faces, face2str)
		]
		out = open(filename, "w")
		for name, items, str_fun in parts:
			for item in items:
				out.write(name)
				for sub in item:
					out.write(" ")
					out.write(str_fun(sub))
				out.write("\n")
		out.close()



class Squeeze(Entity):

	def __init__(self, obj_name):
		Entity.__init__(self)
		self.obj = ObjObject(obj_name)

	def render_sub(self):
		glColor(1, 1, 0)
		self.obj.render()

	def update_sub(self, time_dif):
		if Stupid.key_state(K_p, True):
			self.obj.save("tmp.obj")


if __name__ == "__main__":

	stupid = Stupid("Stupid [ CGI - Aufgabe 3 ]")
	stupid.add(Squeeze(sys.argv[1]))
	stupid.mainloop()


