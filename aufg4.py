#!/usr/bin/python
# -*- coding: utf8 -*-
import sys,math
from random import Random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from stupid import Stupid, Entity
import font, savage as shit
from vec import vec
class Wave(Entity):
	def __init__(self):
		Entity.__init__(self)
		self.o=shit.Orb(.1,3).gen_list()
		self.p=p=[vec(*map(float,l.split()))for l in open("wave.txt")]
		m=[];exec"m=[1]+map(sum,zip(m,m[1:]))+[1];"*~-len(p);self.m=m
		self.f=0
	def update_sub(self,time_dif):self.f^=Stupid.key_state(K_t,1)
	def b(self,t):
		p=self.p;l=len(p)
		return sum((c*(1-t)**i*x*t**(l-i-1)for i,x,c in zip(range(l),p,self.m)),vec())
	def l(self,t):
		p=self.p;l=len(p);r=range(l)
		return sum((x*reduce(float.__mul__,((t*~-l-k)/(i-k+.0)for k in r if i-k))for i,x in zip(r,p)),vec())
	def render_sub(self):
		for _ in[GL_LIGHTING,GL_DEPTH_TEST]:glDisable(_)
		p=self.p
		glLineWidth(1);glColor(.5,.5,.3)
		glBegin(GL_LINE_STRIP)
		for x in p:glVertex(x)
		glEnd()
		f=[self.l,self.b][self.f];t=0
		glLineWidth(5);glColor(0,0,0)
		glBegin(GL_LINE_STRIP)
		while t<=1:glVertex(f(t));t+=.01
		glEnd()
		glColor(1,1,1)
		for x in p:glPushMatrix();glTranslate(*x);glCallList(self.o);glPopMatrix()
if __name__ == "__main__":
	stupid = Stupid("Stupid [ CGI - Aufgabe 4 ]")
	stupid.add(Wave())
	stupid.mainloop()
