#!/usr/bin/python
# -*- coding: utf8 -*-

import math
import sys
from random import Random

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from stupid import Stupid, Entity
import font
import savage as shit
from vec import vec


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
			"f" : lambda x : f.append([face_voodoo(i) for i in x])
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


	def calc_triangles(self):
		# triangulation works only for convex polygons atm
		triangles = []
		for f in [[vec(*self.vertices[v[0] - 1]) for v in face] for face in self.faces]:
			a = f[0]
			for b, c in zip(f[1:], f[2:]): triangles.append([a, b, c])
		return triangles


	def calc_surface(self):
		def triangle_surface(tri):
			a = (tri[1] - tri[0]).length()
			b = (tri[2] - tri[1]).length()
			c = (tri[0] - tri[2]).length()
			s = (a + b + c) * 0.5
			return (s * (s - a) * (s - b) * (s - c)) ** 0.5
		return sum(triangle_surface(t) for t in self.calc_triangles())


	def calc_volume(self):
		return (1 / 6.0) * sum(a.dot(b.cross(c)) for a, b, c in self.calc_triangles())


#	def erase_normals(self):
#		self.normals = []
#		for face in self.faces:
#			for i, (v, t, _) in enumerate(face): face[i] = v, t, None


	def noise(self, sigma):
		rand = Random()
		self.vertices = [tuple(rand.gauss(x, sigma) for x in vertex) for vertex in self.vertices]
		self.gen_list()


	def smooth(self, alpha, depth=1):
		vec_verts = [vec(*vert) for vert in self.vertices]
		faces_indices = [[x[0] for x in face] for face in self.faces]
		lookup = []
		for i, v in enumerate(vec_verts):
			neighbors = set()
			lookup.append(neighbors)
			i += 1
			for face in faces_indices:
				if i in face:
					q = face.index(i)
					neighbors.add(vec_verts[face[q - 1] - 1])
					neighbors.add(vec_verts[face[q + 1 - len(face)] - 1])

		for _ in range(depth):
			self.vertices = []
			for i, neighbors in enumerate(lookup):
				balance = vec()
				for n in neighbors: balance += n
				balance *= 1.0 / len(neighbors)
				v = alpha * vec_verts[i] + (1 - alpha) * balance
				self.vertices.append((v.x, v.y, v.z))
		self.gen_list()



class Squeeze(Entity):

	def __init__(self, obj_name):
		Entity.__init__(self)

		self.obj = ObjObject(obj_name)

		self.surface = 0
		self.volume = 0
		self.sigma = 0.01
		self.alpha = 0.3


	def render_sub(self):
		glColor(1, 1, 0)
		self.obj.render()

		glColor(1, 1, 1)
		font.put(5, 100, "surface: %s" % self.surface)
		font.put(5, 110, "volume:  %s" % self.volume)
		font.put(5, 120, "sigma:   %.2f" % self.sigma)
		font.put(5, 130, "alpha:   %.2f" % self.alpha)



	def update_sub(self, time_dif):

		if Stupid.key_state(K_p, True):
			self.obj.save("tmp.obj")

		if Stupid.key_state(K_y, True):
			self.volume = self.obj.calc_volume()
		if Stupid.key_state(K_x, True):
			self.surface = self.obj.calc_surface()

		if Stupid.key_state(K_c, True):
			self.obj.noise(self.sigma)
		if Stupid.key_state(K_v, True):
			self.obj.smooth(self.alpha)


		self.sigma += (Stupid.key_state(K_r, True) - Stupid.key_state(K_f, True)) * 0.01
		self.alpha += (Stupid.key_state(K_t, True) - Stupid.key_state(K_g, True)) * 0.01




if __name__ == "__main__":

	stupid = Stupid("Stupid [ CGI - Aufgabe 3 ]")
	stupid.add(Squeeze(sys.argv[1]))
	stupid.mainloop()


