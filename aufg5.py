#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from stupid import Stupid, Entity
import math
import font
import savage as shit
from vec import vec

from aufg3 import ObjObject


class Shade:
	def __init__(self, v_code, f_code):
		self.shadow_prog = glCreateProgram()
		for c, t in (v_code, GL_VERTEX_SHADER), (f_code, GL_FRAGMENT_SHADER):
			shader = glCreateShader(t)
			glShaderSource(shader, c)
			glCompileShader(shader)
			print glGetShaderInfoLog(shader)
			glAttachShader(self.shadow_prog, shader)
			glDeleteShader(shader)
		glLinkProgram(self.shadow_prog)
	def on(self): glUseProgram(self.shadow_prog)
	def off(self): glUseProgram(GL_NONE)

class Trick(Entity):
	def __init__(self, obj_name):
		Entity.__init__(self)
		self.obj = ObjObject(obj_name)

		v = """void main() {
			gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
		}"""
		f = """void main() {
			gl_FragColor = vec4(1, 0.6, 0.8, 0.1);
		}"""
		self.shade = Shade(v, f)

	def render_sub(self):
		self.shade.on()
		glColor(1, 0, 1)
		self.obj.render()



if __name__ == "__main__":

	stupid = Stupid("Stupid [ CGI - Aufgabe 5 ]")
	stupid.add(Trick(sys.argv[1]))
	stupid.mainloop()


