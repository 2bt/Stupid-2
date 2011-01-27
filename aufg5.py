#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from stupid import Stupid, Entity
import font
import savage as shit
from vec import vec

from aufg3 import ObjObject


class Shade:
	def __init__(self, v_code, f_code):
		self.prog = glCreateProgram()
		for c, t in (v_code, GL_VERTEX_SHADER), (f_code, GL_FRAGMENT_SHADER):
			shader = glCreateShader(t)
			glShaderSource(shader, c)
			glCompileShader(shader)
			print glGetShaderInfoLog(shader)
			glAttachShader(self.prog, shader)
			glDeleteShader(shader)
		glLinkProgram(self.prog)
		self.locations = {}

	def get_location(self, name):
		if name not in self.locations:
			self.locations[name] = glGetUniformLocation(self.prog, name)
		return self.locations[name]

	def uniformf(self, name, *value):
		l = self.get_location(name)
		eval("glUniform%df"%len(value))(l, *value)	#wtf

	def uniformi(self, name, *value):
		l = self.get_location(name)
		eval("glUniform%di"%len(value))(l, *value)	#wtf


	def on(self): glUseProgram(self.prog)

	def off(self): glUseProgram(GL_NONE)

class Trick(Entity):
	def __init__(self, obj_name):
		Entity.__init__(self)
		self.obj = ObjObject(obj_name)

		v = """
uniform vec3 light_pos;

varying vec3 pos, eye, normal, lpos, light_diff;
void main(void) {
	pos = gl_Vertex.xyz;
	lpos = vec3(gl_ModelViewMatrix * vec4(light_pos, 0.0));
	eye = vec3(gl_ModelViewMatrix * gl_Vertex);
	light_diff = pos - light_pos;
	normal = gl_NormalMatrix * gl_Normal;
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}"""

		f = """
uniform bool blinn;
uniform float shininess, sections;
uniform vec4 color, diffuse, ambient, specular;

varying vec3 pos, normal, eye, light_diff;
void main(void) {
	vec3 n = normalize(normal);
	vec3 ldir = normalize(-light_diff);
	vec3 vdir = normalize(eye);
	vec3 lhalf = normalize(ldir - vdir);
	vec4 cl = color;
	float intensity = max(dot(n, ldir), 0.0);

	float foo;
	if (blinn) foo = max(dot(n, lhalf), 0.0);
	else  foo = max(dot(vdir, reflect(ldir, n)), 0.0);      

	intensity = floor(intensity * sections) / sections;
	foo = pow(foo, shininess);
	foo = foo > 0.1 ? 1.0 : 0.0;

	cl *= ambient;
	cl += specular * foo;
	cl *= diffuse * intensity;

	gl_FragColor = cl;

	gl_FragColor = color;

}
"""
		self.shade = Shade(v, f)

	def render_sub(self):

		self.shade.on()
		self.shade.uniformf("light_pos", 50, 50, 50)
		self.shade.uniformi("blinn", 1)
		self.shade.uniformf("shininess", 1)
		self.shade.uniformf("sections", 1)
		self.shade.uniformf("color", 1, 0, 1, 1)
		self.shade.uniformf("diffuse", 1, 1, 1, 1)
		self.shade.uniformf("ambient", 1, 1, 1, 1)
		self.shade.uniformf("specular", 1, 1, 1, 1)
		self.obj.render()
		self.shade.off()



if __name__ == "__main__":

	stupid = Stupid("Stupid [ CGI - Aufgabe 5 ]")
	stupid.add(Trick(sys.argv[1]))
	stupid.mainloop()


