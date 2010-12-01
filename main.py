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
		b = shit.Brick(1, 1, 1)
		self.cubes = b.gen_list(), b.scale(-1, -1, -1).gen_list()
		self.orb = shit.Orb(0.1).gen_list()

		self.p = vec(0, 0, -0.5)
		self.bfc = False
		self.inverse = False

	def update_sub(self, time_dif):
		self.p.x += (Stupid.key_state(K_r) - Stupid.key_state(K_f)) * time_dif
		self.p.y += (Stupid.key_state(K_t) - Stupid.key_state(K_g)) * time_dif
		self.p.z += (Stupid.key_state(K_z) - Stupid.key_state(K_h)) * time_dif
		if Stupid.key_state(K_b, True): self.bfc = not self.bfc
		if Stupid.key_state(K_i, True): self.inverse = not self.inverse


	def render_sub(self):

		glPushMatrix()
		p = self.p
		if self.inverse: p = -p
		glMultMatrixf([
			1, 0, 0, p.x,
			0, 1, 0, p.y,
			0, 0, 1, p.z,
			0, 0, 0, 1
		])

		glColor(1, 1, 0)
		glCallList(self.cubes[self.bfc])
		glPopMatrix()

		if p.x:
			glColor(1, 0, 0)
			glPushMatrix()
			glTranslate(1/p.x, 0, 0)
			glCallList(self.orb)
			glPopMatrix()

		if p.y:
			glColor(0, 1, 0)
			glPushMatrix()
			glTranslate(0, 1/p.y, 0)
			glCallList(self.orb)
			glPopMatrix()

		if p.z:
			glColor(0, 0, 1)
			glPushMatrix()
			glTranslate(0, 0, 1/p.z)
			glCallList(self.orb)
			glPopMatrix()

		glColor(1, 1, 1)
		font.put(5, 100, str(self.p))
		font.put(5, 110, "bfc: %s" % self.bfc)
		font.put(5, 120, "inverse: %s" % self.bfc)


class Suck(Entity):

	def __init__(self):
		Entity.__init__(self)

		img = pygame.image.load('gorilla.bmp')
		data = pygame.image.tostring(img, "RGBA", 1)

		self.tex = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, self.tex)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.get_width(), img.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
		glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, (1, 1, 1, 1))

		self.orb = shit.Orb(5, 3).gen_list()
		self.dot = shit.Orb(0.1).gen_list()

		self.eye = vec(1, 4, 8)
		self.target = vec(0, 0, 0)
		self.up = vec(0, 1, 0)

		self.q = 0

	def update_sub(self, time_dif):
		d = vec(
			Stupid.key_state(K_h) - Stupid.key_state(K_f),
			Stupid.key_state(K_r) - Stupid.key_state(K_z),
			Stupid.key_state(K_g) - Stupid.key_state(K_t),
		) * time_dif * 10

		self.q = (self.q + Stupid.key_state(K_c, True)) % 3
		[self.eye, self.target, self.up][self.q] += d

	def render_sub(self):

		glPushAttrib(GL_ALL_ATTRIB_BITS)

		glPushMatrix()
		glLoadIdentity()
		glTranslate(0.5, 0.5, 0)
#		gluPerspective(45*2, 1, 1, 1000)
		gluLookAt(self.eye.x, self.eye.y, self.eye.z,
			self.target.x, self.target.y, self.target.z,
			self.up.x, self.up.y, self.up.z)
		mvm = glGetFloatv(GL_MODELVIEW_MATRIX)
		glPopMatrix()

		mvm = zip(*mvm)

		glBindTexture(GL_TEXTURE_2D, self.tex)
		glEnable(GL_TEXTURE_2D)
		glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)
		glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)
		glTexGenfv(GL_S, GL_OBJECT_PLANE, mvm[0])
		glTexGenfv(GL_T, GL_OBJECT_PLANE, mvm[1])

		glEnable(GL_TEXTURE_GEN_S)
		glEnable(GL_TEXTURE_GEN_T)

		glColor(0.5, 0.5, 1)
		glCallList(self.orb)

		glPopAttrib(GL_ALL_ATTRIB_BITS)

		glColor(1, 0, 0)
		glPushMatrix()
		glTranslate(*self.eye)
		glCallList(self.dot)
		glPopMatrix()

		glLineWidth(3)
		glDisable(GL_LIGHTING)
		glBegin(GL_LINES)
		glVertex(self.eye)
		glVertex(self.target)
		glEnd()
		glEnable(GL_LIGHTING)

		glColor(1, 1, 1)
		font.put(5, 100, "eye: %s" % self.eye)
		font.put(5, 110, "target: %s" % self.target)
		font.put(5, 120, "up: %s" % self.up)



if __name__ == "__main__":

	stupid = Stupid("Stupid [ CGI - Aufgabe 2 ]")
	stupid.add(Suck())
	stupid.add(Contra())
	stupid.mainloop()


