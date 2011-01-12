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



class Wave(Entity):
	def __init__(self):
		Entity.__init__(self)

		self.o=shit.Orb(.1,3).gen_list()
		self.f=Wave.b;
		self.p=p=[vec(*map(float,l.split()))for l in open("wave.txt")]
		m=[];exec"m=[1]+map(sum,zip(m,m[1:]))+[1];"*~-len(p);self.m=m

	def update_sub(self,time_dif):pass

	def b(self,u):
		p=self.p;l=len(p)
		return reduce(vec.__add__,(c*(1-u)**i*x*u**(l-i-1)for i,x,c in zip(range(l),p,self.m)))

	def render_sub(self):
		glDisable(GL_LIGHTING)
		glDisable(GL_DEPTH_TEST)

		p=self.p
		glLineWidth(1)
		glColor(.5,.5,.3)
		glBegin(GL_LINE_STRIP)
		for x in p:glVertex(x)
		glEnd()

		glLineWidth(5)
		glColor(0,0,0)
		u=0
		glBegin(GL_LINE_STRIP)
		while u<=1:glVertex(self.f(self,u));u+=.01
		glEnd()

		glColor(1,1,1)
		for x in p:glPushMatrix();glTranslate(*x);glCallList(self.o);glPopMatrix()

		glEnable(GL_DEPTH_TEST)
		glEnable(GL_LIGHTING)

if __name__ == "__main__":
	stupid = Stupid("Stupid [ CGI - Aufgabe 4 ]")
	stupid.add(Wave())
	stupid.mainloop()
